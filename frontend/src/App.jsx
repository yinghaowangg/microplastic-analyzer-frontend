import { Routes, Route } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import ReportPage from "./pages/ReportPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<UploadPage />} />
      <Route path="/report" element={<ReportPage />} />
    </Routes>
  );
}