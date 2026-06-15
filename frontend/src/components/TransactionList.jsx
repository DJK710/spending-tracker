import { useState } from "react";

function TransactionList({ transactions, onEdit, onDelete }) {
  const [typeFilter, setTypeFilter] = useState("all");
  const [subscriptionFilter, setSubscriptionFilter] = useState("all");
  const [sortBy, setSortBy] = useState("newest");

  const filteredTransactions = transactions
    .filter((transaction) => {
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

      if (sortBy === "newest") {
        return new Date(b.transaction_date) - new Date(a.transaction_date);
      }

      if (sortBy === "oldest") {
        return new Date(a.transaction_date) - new Date(b.transaction_date);
      }

      return 0;
    });

  const transactionTypes = [
    ...new Set(transactions.map((transaction) => transaction.type)),
  ];

  return (
    <div className="transaction-list">
      <div className="filters">
        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
          <option value="all">All types</option>
          {transactionTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>

        <select
          value={subscriptionFilter}
          onChange={(e) => setSubscriptionFilter(e.target.value)}
        >
          <option value="all">All transactions</option>
          <option value="subscriptions">Subscriptions only</option>
          <option value="non-subscriptions">No subscriptions</option>
        </select>

        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="newest">Newest first</option>
          <option value="oldest">Oldest first</option>
          <option value="amount-high">Highest amount</option>
          <option value="amount-low">Lowest amount</option>
        </select>
      </div>

      {filteredTransactions.map((transaction) => (
        <div key={transaction.id} className="transaction-card">
            <p>{transaction.description}</p>
            <p>€{transaction.amount}</p>
            <p>{transaction.type}</p>
            <p>{transaction.transaction_date}</p>
            <div className="transaction-actions">
                <button type="button" onClick={()=> onEdit(t)}>
                    Edit
                </button>

                <button type="button" onClick={()=> onDelete(t.id)}>
                    Delete
                </button>
            </div>
        </div>
      ))}
    </div>
  );
}

export default TransactionList;