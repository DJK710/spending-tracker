import { useEffect, useState } from "react";
import api from "../api";

function RecurringPage({ onTransactionsChanged }) {
  const [series, setSeries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [markingKey, setMarkingKey] = useState(null);

  const fetchSeries = async () => {
    setIsLoading(true);

    try {
      const res = await api.get("/recurring/detect");
      setSeries(res.data);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSeries();
  }, []);

  const totalMonthlyCost = series.reduce(
    (sum, item) => sum + Math.abs(item.avg_amount),
    0
  );

  const markAsSubscription = async (item) => {
    const key = item.transaction_ids.join(",");
    setMarkingKey(key);

    try {
      await api.post("/transactions/bulk-subscription-flag", {
        transaction_ids: item.transaction_ids,
        is_subscription: true,
      });

      await fetchSeries();
      await onTransactionsChanged?.();
    } finally {
      setMarkingKey(null);
    }
  };

  return (
    <div className="recurring-page">
      <div className="card">
        <div className="recurring-summary">
          <span>Total recurring monthly cost</span>
          <strong>€{totalMonthlyCost.toFixed(2)}</strong>
          <p>
            Detected from transaction history: same description, similar amount, roughly
            monthly cadence.
          </p>
        </div>
      </div>

      {isLoading && <p>Detecting recurring charges...</p>}

      {!isLoading && series.length === 0 && (
        <p>No recurring charges detected yet.</p>
      )}

      <div className="recurring-list">
        {series.map((item) => {
          const key = item.transaction_ids.join(",");

          return (
            <div key={key} className="recurring-card">
              <div className="recurring-info">
                <strong>{item.description}</strong>
                <span>
                  {item.type} &middot; €{Math.abs(item.avg_amount).toFixed(2)} &middot;{" "}
                  {item.occurrence_count} charges
                </span>
                <p>Last charged: {item.last_date}</p>
                <p>Predicted next charge: {item.predicted_next_date}</p>
              </div>

              <div className="recurring-actions">
                <button
                  type="button"
                  onClick={() => markAsSubscription(item)}
                  disabled={item.all_marked_subscription || markingKey === key}
                >
                  {item.all_marked_subscription
                    ? "Already marked"
                    : markingKey === key
                    ? "Marking..."
                    : "Mark as subscription"}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default RecurringPage;
