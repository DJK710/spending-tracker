import { useEffect, useState } from "react";
import api from "../api";

const emptyForm = {
  keywords: "",
  transactionType: "",
  isSubscription: false,
  subscriptionKeywords: "",
  amountSign: "any",
  isActive: true,
};

function splitKeywords(value) {
  return value
    .split(",")
    .map((keyword) => keyword.trim())
    .filter((keyword) => keyword.length > 0);
}

function CategorizationRulesPage({ onTransactionsChanged }) {
  const [rules, setRules] = useState([]);
  const [editingRuleId, setEditingRuleId] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [reapplyMessage, setReapplyMessage] = useState("");
  const [isReapplying, setIsReapplying] = useState(false);
  const [error, setError] = useState("");

  const fetchRules = async () => {
    const res = await api.get("/categorization-rules/");
    setRules(res.data);
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const resetForm = () => {
    setForm(emptyForm);
    setEditingRuleId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    const payload = {
      keywords: splitKeywords(form.keywords),
      transaction_type: form.transactionType,
      is_subscription: form.isSubscription,
      subscription_keywords: form.subscriptionKeywords
        ? splitKeywords(form.subscriptionKeywords)
        : null,
      amount_sign: form.amountSign,
      is_active: form.isActive,
    };

    if (payload.keywords.length === 0) {
      setError("Enter at least one keyword.");
      return;
    }

    try {
      if (editingRuleId) {
        await api.put(`/categorization-rules/${editingRuleId}`, payload);
      } else {
        const nextPriority =
          rules.length > 0 ? Math.max(...rules.map((rule) => rule.priority)) + 10 : 10;
        await api.post("/categorization-rules/", { ...payload, priority: nextPriority });
      }

      resetForm();
      await fetchRules();
    } catch (submitError) {
      setError(submitError.response?.data?.detail || "Could not save this rule.");
    }
  };

  const startEditing = (rule) => {
    setEditingRuleId(rule.id);
    setForm({
      keywords: rule.keywords.join(", "),
      transactionType: rule.transaction_type,
      isSubscription: rule.is_subscription,
      subscriptionKeywords: (rule.subscription_keywords || []).join(", "),
      amountSign: rule.amount_sign,
      isActive: rule.is_active,
    });
  };

  const deleteRule = async (ruleId) => {
    await api.delete(`/categorization-rules/${ruleId}`);

    if (editingRuleId === ruleId) {
      resetForm();
    }

    await fetchRules();
  };

  const moveRule = async (index, direction) => {
    const targetIndex = index + direction;

    if (targetIndex < 0 || targetIndex >= rules.length) {
      return;
    }

    const reordered = [...rules];
    [reordered[index], reordered[targetIndex]] = [reordered[targetIndex], reordered[index]];

    await api.post("/categorization-rules/reorder", {
      ordered_ids: reordered.map((rule) => rule.id),
    });

    await fetchRules();
  };

  const reapplyRules = async () => {
    setIsReapplying(true);
    setReapplyMessage("");

    try {
      const res = await api.post("/categorization-rules/reapply");
      setReapplyMessage(`Updated ${res.data.updated_count} existing transaction(s).`);
      await onTransactionsChanged?.();
    } finally {
      setIsReapplying(false);
    }
  };

  return (
    <div className="rules-page">
      <div className="card">
        <form className="form" onSubmit={handleSubmit}>
          <h2>{editingRuleId ? "Edit rule" : "Add rule"}</h2>

          <div>
            <label>Keywords</label>
            <input
              type="text"
              value={form.keywords}
              onChange={(e) => setForm({ ...form, keywords: e.target.value })}
              placeholder="netflix, netflix.com (comma-separated)"
              required
            />
          </div>

          <div>
            <label>Category</label>
            <input
              type="text"
              value={form.transactionType}
              onChange={(e) => setForm({ ...form, transactionType: e.target.value })}
              placeholder="e.g. Netflix, Groceries"
              required
            />
          </div>

          <div>
            <label>Subscription</label>
            <input
              type="checkbox"
              checked={form.isSubscription}
              onChange={(e) => setForm({ ...form, isSubscription: e.target.checked })}
            />
          </div>

          <div>
            <label>Also subscription if text contains</label>
            <input
              type="text"
              value={form.subscriptionKeywords}
              onChange={(e) => setForm({ ...form, subscriptionKeywords: e.target.value })}
              placeholder="optional, e.g. recurring, membership"
            />
          </div>

          <div>
            <label>Amount sign</label>
            <select
              value={form.amountSign}
              onChange={(e) => setForm({ ...form, amountSign: e.target.value })}
            >
              <option value="any">Any</option>
              <option value="positive">Positive only (income/refund)</option>
              <option value="negative">Negative only (expense)</option>
            </select>
          </div>

          <div>
            <label>Active</label>
            <input
              type="checkbox"
              checked={form.isActive}
              onChange={(e) => setForm({ ...form, isActive: e.target.checked })}
            />
          </div>

          <div className="rule-form-actions">
            <button type="submit">{editingRuleId ? "Update rule" : "Add rule"}</button>

            {editingRuleId && (
              <button type="button" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>

          {error && <p className="error-message">{error}</p>}
        </form>
      </div>

      <div className="card">
        <div className="rules-reapply">
          <div>
            <h2>Re-apply rules to existing transactions</h2>
            <p>
              Only checks each transaction's description &mdash; rules that depended on bank
              remittance details may not re-match older imports.
            </p>
          </div>

          <button type="button" onClick={reapplyRules} disabled={isReapplying}>
            {isReapplying ? "Re-applying..." : "Re-apply rules"}
          </button>
        </div>

        {reapplyMessage && <p className="upload-message">{reapplyMessage}</p>}
      </div>

      <div className="rule-list">
        {rules.map((rule, index) => (
          <div key={rule.id} className="rule-card">
            <div className="rule-info">
              <strong>{rule.transaction_type}</strong>
              <span>{rule.keywords.join(", ")}</span>

              {rule.subscription_keywords?.length > 0 && (
                <p>Subscription if also contains: {rule.subscription_keywords.join(", ")}</p>
              )}

              <p>
                {rule.is_subscription ? "Always subscription" : "Not subscription by default"} &middot;
                {" "}
                {rule.amount_sign === "any" ? "Any amount" : `${rule.amount_sign} amount only`}
                {!rule.is_active && " · Inactive"}
              </p>
            </div>

            <div className="rule-actions">
              <button type="button" onClick={() => moveRule(index, -1)} disabled={index === 0}>
                Up
              </button>

              <button
                type="button"
                onClick={() => moveRule(index, 1)}
                disabled={index === rules.length - 1}
              >
                Down
              </button>

              <button type="button" onClick={() => startEditing(rule)}>
                Edit
              </button>

              <button type="button" onClick={() => deleteRule(rule.id)}>
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CategorizationRulesPage;
