import React, { useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './App.css';

// Register chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const App = () => {
  const [status, setStatus] = useState("");
  const [item, setItem] = useState("");
  const [quantity, setQuantity] = useState("");
  const [orderDetails, setOrderDetails] = useState([]);
  const [orderHistory, setOrderHistory] = useState([]);

  // Function to handle order placement
  const handlePlaceOrder = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/order', {
        order: { item, quantity: parseInt(quantity) }
      });
      setOrderDetails([...orderDetails, { item, quantity: parseInt(quantity), message: response.data.message }]);
      setStatus(response.data.message);
      updateOrderHistory(item, quantity, response.data.message);
    } catch (error) {
      console.error("Error placing order:", error);
      setStatus("Failed to place order");
    }
  };

  // Function to update order history
  const updateOrderHistory = (item, quantity, message) => {
    setOrderHistory(prevHistory => [
      ...prevHistory,
      { item, quantity, status: message }
    ]);
  };

  // Function to send materials
  const sendMaterials = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/send_materials');
      setStatus(response.data.message);
    } catch (error) {
      console.error("Error sending materials:", error);
      setStatus("Failed to send materials");
    }
  };

  // Function to manufacture goods
  const manufactureGoods = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/manufacture_goods');
      setStatus(response.data.message);
    } catch (error) {
      console.error("Error manufacturing goods:", error);
      setStatus("Failed to manufacture goods");
    }
  };

  // Function to distribute goods
  const distributeGoods = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/distribute_goods');
      setStatus(response.data.message);
    } catch (error) {
      console.error("Error distributing goods:", error);
      setStatus("Failed to distribute goods");
    }
  };

  // Function to confirm order
  const confirmOrder = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/confirm_order');
      setStatus(response.data.message);
    } catch (error) {
      console.error("Error confirming order:", error);
      setStatus("Failed to confirm order");
    }
  };

  // Function to check status
  const checkStatus = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/status');
      setStatus(response.data.status);
    } catch (error) {
      console.error("Error checking status:", error);
      setStatus("Failed to check status");
    }
  };

  // Prepare data for the graph
  const data = {
    labels: orderHistory.map((order, index) => `Order ${index + 1}`),
    datasets: [
      {
        label: 'Order Quantities',
        data: orderHistory.map(order => order.quantity),
        borderColor: '#4A90E2',
        backgroundColor: 'rgba(74, 144, 226, 0.2)',
        fill: true,
      },
    ],
  };

  return (
    <div className="app-container">
      <div className="glassmorphism-card">
        <h1 className="title">Supply Chain Management Dashboard</h1>
        
        <div className="input-container">
          <label htmlFor="item">Order Item:</label>
          <input
            type="text"
            id="item"
            value={item}
            onChange={(e) => setItem(e.target.value)}
            placeholder="Enter item name"
          />
        </div>
        
        <div className="input-container">
          <label htmlFor="quantity">Order Quantity:</label>
          <input
            type="number"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            placeholder="Enter quantity"
          />
        </div>

        <div className="button-container">
          <button onClick={handlePlaceOrder}>Place Order</button>
          <button onClick={sendMaterials}>Send Materials</button>
          <button onClick={manufactureGoods}>Manufacture Goods</button>
          <button onClick={distributeGoods}>Distribute Goods</button>
          <button onClick={confirmOrder}>Confirm Order</button>
          <button onClick={checkStatus}>Check Status</button>
        </div>

        <div className="order-details">
          <h2>Order History</h2>
          <ul>
            {orderDetails.map((order, index) => (
              <li key={index}>
                <strong>Item:</strong> {order.item} | <strong>Quantity:</strong> {order.quantity} | <strong>Status:</strong> {order.message}
              </li>
            ))}
          </ul>
        </div>

        <p className="status">Current Status: {status}</p>

        <div className="chart-container">
          <h2>Order Quantity Trend</h2>
          <Line data={data} />
        </div>
      </div>
    </div>
  );
};

export default App;
