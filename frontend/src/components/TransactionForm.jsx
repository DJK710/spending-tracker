import { useEffect, useState } from "react";

function TransactionForm({onTransactionCreated, onEdit, editingTransaction}) {
    const [amount, setAmount] = useState("");
    const [type, setType] = useState("");
    const [description, setDescription] = useState("");
    const [subscription, setSubscription] = useState(false);

    const handleSubmit = async (e) => {
    e.preventDefault();

    const newTransaction =  {
        amount: Number(amount),
        type,
        description,
        is_subscription: subscription
    };

    if (editingTransaction) {
        await onEdit(editingTransaction.id, newTransaction)
    } else {
        await onTransactionCreated(newTransaction)
    }

    setAmount("");
    setType("");
    setDescription("");
    setSubscription(false);
    };

    useEffect(() => {
        if (editingTransaction) {
            setAmount(editingTransaction.amount);
            setType(editingTransaction.type);
            setDescription(editingTransaction.description);
            setSubscription(editingTransaction.is_subscription);
        }
    }, [editingTransaction]);

    return (
        <form onSubmit={handleSubmit} className="transaction-form">
            <h2>Add Transaction</h2>

            <div>
                <label>Amount</label>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                />
            </div>

            <div>
                <label>Type</label>
                <input
            type="text"
            value={type}
            onChange={(e) => setType(e.target.value)}
            placeholder="e.g. groceries, gaming"
            required
            />
    </div>

    <div>
      <label>Description</label>
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
    </div>

    <div>
      <label>Subscription</label>
      <input
        type="checkbox"
        checked={subscription}
        onChange={(e) => setSubscription(e.target.checked)}
      />
    </div>

    <button type="submit">
        {editingTransaction ? "Update transaction" : "Add Transaction"}
    </button>
  </form>
);
}

export default TransactionForm