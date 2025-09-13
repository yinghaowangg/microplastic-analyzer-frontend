
import "../styles/LoadingOverlay.css";

export default function LoadingOverlay() {
  return (
    <div className="loading-overlay">
      <div className="energy-ring"></div>
      <p lassName="loading-text">智能分析中…</p>
    </div>
  );
}