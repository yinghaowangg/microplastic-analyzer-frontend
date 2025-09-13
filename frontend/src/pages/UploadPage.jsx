// src/pages/UploadPage.jsx
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";
import { motion } from "framer-motion";
import LoadingOverlay from "../components/LoadingOverlay";
import "../styles/UploadPage.css";

export default function UploadPage() {
  const [fileName, setFileName] = useState("");
  const [previewURL, setPreview] = useState(null); // 预览地址
  const [loading, setLoading] = useState(false);
  const fileRef = useRef(null);
  const navigate = useNavigate();

  /* 选中文件时生成本地预览 URL */
  const handleFileChange = () => {
    const file = fileRef.current?.files[0];
    if (!file) return;
    setFileName(file.name);
    setPreview(URL.createObjectURL(file)); // 生成临时预览地址
  };

  /* 点击分析 */
  const handleAnalyze = () => {
    const file = fileRef.current?.files[0];
    if (!file) return alert("请上传图像文件");

    setLoading(true);

    // 跳转到 ReportPage，并传递 file 和预览地址
    navigate("/report", {
      state: {
        file,                        // 真正的文件对象（ReportPage 会上传给后端）
        input_image: previewURL      // 预览图 URL（本地显示用）
      }
    });

    setLoading(false);
  };

  /* 离开组件时释放 blob URL */
  useEffect(() => {
    return () => {
      if (previewURL?.startsWith("blob:")) URL.revokeObjectURL(previewURL);
    };
  }, [previewURL]);

  /* 粒子背景初始化 */
  const particlesInit = (main) => loadFull(main);

  return (
    <>
      {/* 粒子背景 */}
      <Particles
        id="tsparticles"
        init={particlesInit}
        options={{
          background: { color: "#EFFAF0" },
          fpsLimit: 60,
          particles: {
            number: { value: 45 },
            color: { value: "#4caf50" },
            shape: { type: "circle" },
            opacity: { value: 0.28 },
            size: { value: 2 },
            links: {
              enable: true,
              distance: 100,
              color: "#4caf50",
              opacity: 0.35,
              width: 0.8
            },
            move: { enable: true, speed: 0.6, outModes: "bounce" }
          }
        }}
        style={{ position: "absolute", zIndex: 0, pointerEvents: "none" }}
      />

      {/* 叶子装饰 */}
      <div className="leaf-decor left">🍃</div>
      <div className="leaf-decor right">🍃</div>

      {/* 主体 */}
      <div className="page-wrapper">
        <motion.div
          className="wrapper"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <header>
            <img src="/image/jycollege-logo.jpeg" className="logo" alt="logo" />
            <h1 className="glow-text">微塑料图像智能分析平台</h1>
            <p className="tagline">绿色可持续发展 · 创新未来</p>
            <p>智能识别 · 环保研究 · 学术实践</p>
          </header>

          <div className="container">
            <h2>📤 上传检测图像</h2>

            <div className="upload-box">
              <label className="file-label">
                <i className="fa fa-folder-open" />
                选择图像文件
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                />
              </label>
            </div>

            <div className="file-name-display">{fileName}</div>

            {/* 预览图 */}
            {previewURL && (
              <img src={previewURL} alt="预览" className="preview-thumb" />
            )}

            <button className="StartAnalysisButton" onClick={handleAnalyze}>
              上传并分析 <i className="fa fa-arrow-right icon-right" />
            </button>
          </div>
        </motion.div>
      </div>

      {/* 波浪装饰 */}
      <div className="wave_container">
        <div className="wave"></div>
        <div className="wave"></div>
        <div className="wave"></div>
      </div>

      {/* 加载遮罩 */}
      {loading && <LoadingOverlay />}
    </>
  );
}