import { useEffect, useState } from "react";

export default function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");

  const load = () =>
    fetch("/api/items").then((r) => r.json()).then(setItems);

  useEffect(() => { load(); }, []);

  const add = async () => {
    if (!name) return;
    await fetch("/api/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    setName("");
    load();
  };

  return (
    <div style={{ padding: 30, fontFamily: "sans-serif" }}>
      <h1>Project 20: React + FastAPI + PostgreSQL</h1>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Add an item" />
      <button onClick={add}>Add</button>
      <ul>{items.map((i) => <li key={i.id}>{i.name}</li>)}</ul>
    </div>
  );
}