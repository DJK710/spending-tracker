import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

function StatsPage({ transactions }) {
  const [selectedMonth, setSelectedMonth] = useState(null);

  const [typeFilter, setTypeFilter] = useState("all");
  const [subscriptionFilter, setSubscriptionFilter] = useState("all");
  const [sortBy, setSortBy] = useState("newest");

  const availableTypes = [
    ...new Set(
      transactions
        .map((transaction) => transaction.type)
        .filter((type) => type && type.toLowerCase() !== "savings")
    ),
  ];

  const filteredTransactions = transactions
    .filter((transaction) => {
      // Always hide Savings from stats
      if (transaction.type?.toLowerCase() === "savings") {
        return false;
      }

      if (typeFilter !== "all" && transaction.type !== typeFilter) {
        return false;
      }

      if (
        subscriptionFilter === "subscriptions" &&
        !transaction.is_subscription
      ) {
        return false;
      }

      if (
        subscriptionFilter === "non-subscriptions" &&
        transaction.is_subscription
      ) {
        return false;
      }

      return true;
    })
    .sort((a, b) => {
      if (sortBy === "amount-high") {
        return Number(b.amount) - Number(a.amount);
      }

      if (sortBy === "amount-low") {
        return Number(a.amount) - Number(b.amount);
      }

      const aDate = a.transaction_date || a.created_at;
      const bDate = b.transaction_date || b.created_at;

      if (sortBy === "newest") {
        return new Date(bDate) - new Date(aDate);
      }

      if (sortBy === "oldest") {
        return new Date(aDate) - new Date(bDate);
      }

      return 0;
    });

  const monthlyStats = getMonthlyStats(filteredTransactions);

  const selectedMonthTransactions = selectedMonth
    ? getTransactionsForMonth(filteredTransactions, selectedMonth)
    : [];

  return (
    <main className="stats-page">
      <section className="stats-section">
        <h2>Filters</h2>

        <div className="filters">
          <select
            value={typeFilter}
            onChange={(event) => setTypeFilter(event.target.value)}
          >
            <option value="all">All types</option>

            {availableTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>

          <select
            value={subscriptionFilter}
            onChange={(event) => setSubscriptionFilter(event.target.value)}
          >
            <option value="all">All transactions</option>
            <option value="subscriptions">Subscriptions only</option>
            <option value="non-subscriptions">No subscriptions</option>
          </select>

          <select
            value={sortBy}
            onChange={(event) => setSortBy(event.target.value)}
          >
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
            <option value="amount-high">Highest amount</option>
            <option value="amount-low">Lowest amount</option>
          </select>
        </div>
      </section>

      <section className="stats-section">
        <h2>Income vs Expenses per Month</h2>

        <div className="chart-card">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyStats}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />

              <Bar
                dataKey="income"
                name="Income"
                fill="#22c55e"
                cursor="pointer"
                onClick={(data) => {
                  setSelectedMonth(data.month);
                }}
              />

              <Bar
                dataKey="expenses"
                name="Expenses"
                fill="#ef4444"
                cursor="pointer"
                onClick={(data) => {
                  setSelectedMonth(data.month);
                }}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {selectedMonth && (
        <section className="stats-section">
          <h2>Transactions for {selectedMonth}</h2>

          <div className="month-transaction-list">
            {selectedMonthTransactions.map((transaction) => (
              <div key={transaction.id} className="month-transaction-card">
                <div>
                  <strong>{transaction.description || "No description"}</strong>
                  <p>{transaction.type}</p>
                </div>

                <div>
                  <strong>€{Number(transaction.amount).toFixed(2)}</strong>
                  <p>
                    {transaction.transaction_date ||
                      transaction.created_at?.slice(0, 10)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

function getMonthlyStats(transactions) {
  const monthlyStats = {};

  transactions.forEach((transaction) => {
    const dateValue = transaction.transaction_date || transaction.created_at;

    if (!dateValue) return;

    const monthKey = dateValue.slice(0, 7);

    if (!monthlyStats[monthKey]) {
      monthlyStats[monthKey] = {
        month: monthKey,
        income: 0,
        expenses: 0,
      };
    }

    const amount = Number(transaction.amount);

    if (amount > 0) {
      monthlyStats[monthKey].income += amount;
    } else {
      monthlyStats[monthKey].expenses += Math.abs(amount);
    }
  });

  return Object.values(monthlyStats).sort((a, b) =>
    a.month.localeCompare(b.month)
  );
}

function getTransactionsForMonth(transactions, selectedMonth) {
  return transactions.filter((transaction) => {
    const dateValue = transaction.transaction_date || transaction.created_at;

    if (!dateValue) return false;

    return dateValue.slice(0, 7) === selectedMonth;
  });
}

export default StatsPage;