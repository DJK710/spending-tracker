import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function AIInsights() {
  const [filters, setFilters] = useState({
    type: "All",
    start_date: "",
    end_date: "",
    subscription_filter: "all",
    sort_by: "newest",
    exclude_savings: true,
  });

  const [insight, setInsight] = useState("");
  const [transactionCount, setTransactionCount] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFilterChange = (event) => {
    const { name, value, type, checked } = event.target;

    setFilters((previousFilters) => ({
      ...previousFilters,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const analyzeSpending = async () => {
    setLoading(true);
    setError("");
    setInsight("");
    setTransactionCount(null);

    try {
      const payload = {
        ...filters,
        start_date: filters.start_date || null,
        end_date: filters.end_date || null,
      };

      const response = await axios.post(
        "http://localhost:8000/ai/analyze",
        payload
      );

      setInsight(response.data.insight);
      setTransactionCount(response.data.transaction_count);
    } catch (err) {
      console.error(err);
      setError("Something went wrong while analyzing your spending.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="ai-insights-card">
      <div className="ai-insights-header">
        <div>
          <h2>AI Spending Insights</h2>
          <p>
            Analyze your transactions using filters, then get a short spending
            summary and saving suggestions.
          </p>
        </div>
      </div>

      <div className="ai-filter-grid">
        <label>
          Type
          <select name="type" value={filters.type} onChange={handleFilterChange}>
            <option value="All">All</option>
            <option value="Groceries">Groceries</option>
            <option value="Gaming">Gaming</option>
            <option value="PayPal">PayPal</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Phone">Phone</option>
            <option value="Savings">Savings</option>
            <option value="Other">Other</option>
          </select>
        </label>

        <label>
          Start date
          <input
            type="date"
            name="start_date"
            value={filters.start_date}
            onChange={handleFilterChange}
          />
        </label>

        <label>
          End date
          <input
            type="date"
            name="end_date"
            value={filters.end_date}
            onChange={handleFilterChange}
          />
        </label>

        <label>
          Subscriptions
          <select
            name="subscription_filter"
            value={filters.subscription_filter}
            onChange={handleFilterChange}
          >
            <option value="all">All</option>
            <option value="subscriptions">Subscriptions only</option>
            <option value="non-subscriptions">Non-subscriptions only</option>
          </select>
        </label>

        <label>
          Sort by
          <select
            name="sort_by"
            value={filters.sort_by}
            onChange={handleFilterChange}
          >
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
            <option value="amount-high">Amount high to low</option>
            <option value="amount-low">Amount low to high</option>
          </select>
        </label>

        <label className="ai-checkbox-label">
          <input
            type="checkbox"
            name="exclude_savings"
            checked={filters.exclude_savings}
            onChange={handleFilterChange}
          />
          Exclude Savings
        </label>
      </div>

      <button
        className="ai-analyze-button"
        onClick={analyzeSpending}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze spending"}
      </button>

      {error && <p className="error-message">{error}</p>}

      {transactionCount !== null && !loading && (
        <p className="ai-transaction-count">
          Analyzed {transactionCount} transaction
          {transactionCount === 1 ? "" : "s"}.
        </p>
      )}

      {insight && (
        <div className="ai-insight-result">
          <ReactMarkdown>{insight}</ReactMarkdown>
        </div>
      )}
    </section>
  );
}

export default AIInsights;