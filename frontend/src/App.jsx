import { useEffect, useState } from "react";
import TransactionForm from "./components/TransactionForm.jsx";
import TransactionList from "./components/TransactionList.jsx";
import StatsPage from "./pages/StatsPage.jsx";
import AIInsights from "./components/AIInsights";
import api from "./api";
import "./App.css";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [currentPage, setCurrentPage] = useState("transactions");

  const fetchTransactions = async () => {
    const res = await api.get("/transactions/");
    setTransactions(res.data);
  };

  const addTransaction = async (newTransaction) => {
    await api.post("/transactions/", newTransaction);
    fetchTransactions();
  };

  const deleteTransaction = async (id) => {
    await api.delete(`/transactions/${id}`);
    fetchTransactions();
  };

  const editTransaction = async (id, transaction) => {
    await api.put(`/transactions/${id}`, transaction);
    fetchTransactions();
    setEditingTransaction(null);
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  return (
    <div className="app">
      <nav className="nav">
        <button onClick={() => setCurrentPage("transactions")}>
          Transactions
        </button>

        <button onClick={() => setCurrentPage("stats")}>Stats</button>
      </nav>

      {currentPage === "transactions" && (
        <>
          <h1>Spending Tracker</h1>

          <div className="card">
            <div className="form">
              <TransactionForm
                onTransactionCreated={addTransaction}
                onEdit={editTransaction}
                editingTransaction={editingTransaction}
              />
            </div>
          </div>

          <div className="transaction-list">
            <h1>Transactions</h1>
            <AIInsights />
            <TransactionList
              transactions={transactions}
              onDelete={deleteTransaction}
              onEdit={setEditingTransaction}
            />
          </div>
        </>
      )}

      {currentPage === "stats" && (
        <>
          <h1>Stats</h1>
          <StatsPage transactions={transactions} />
        </>
      )}
    </div>
  );
}

export default App;