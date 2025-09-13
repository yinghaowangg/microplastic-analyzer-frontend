import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import "../styles/ReportPage.css";

// 注册 Doughnut 所需元素
ChartJS.register(ArcElement, Title, Tooltip, Legend);

export default function ReportPage() {
  const { state } = useLocation();   // 从 UploadPage 传来的数据
  const navigate = useNavigate();

  const [summary, setSummary] = useState({});
  const [outputImage, setOutputImage] = useState(null);
  const [conclusion, setConclusion] = useState("正在加载...");
  const [animatedCount, setAnimatedCount] = useState(0); // 动画数字

  // 文件对象和预览图
  const file = state?.file || null;
  const inputImage = state?.input_image || (file ? URL.createObjectURL(file) : null);

  useEffect(() => {
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    fetch("https://microplastic-analyzer.onrender.com/analyze", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        setSummary(data.summary || {});
        if (data.output_image) {
          setOutputImage(`https://microplastic-analyzer.onrender.com/${data.output_image}`);
        }
        setConclusion(data.conclusion || "未获取到分析结果");
      })
      .catch(err => {
        console.error("分析接口出错", err);
        setConclusion("获取失败，请稍后再试");
      });

    // 清理 blob URL
    return () => {
      if (inputImage?.startsWith("blob:")) URL.revokeObjectURL(inputImage);
    };
  }, [file]);

  const totalCount = Object.values(summary).reduce((a, b) => a + b, 0);

  // 数字动画：0 → totalCount
  useEffect(() => {
    if (totalCount === 0) return;
    let current = 0;
    const step = Math.ceil(totalCount / 20); // 控制动画速度
    const interval = setInterval(() => {
      current += step;
      if (current >= totalCount) {
        current = totalCount;
        clearInterval(interval);
      }
      setAnimatedCount(current);
    }, 80);
    return () => clearInterval(interval);
  }, [totalCount]);

  // 环形图数据
  const chartData = {
    labels: Object.keys(summary),
    datasets: [
      {
        data: Object.values(summary),
        backgroundColor: [
          "#4caf50", // 绿色 → PP
          "#ff9800"  // 橙色 → PS
        ],
        borderWidth: 2,
        borderColor: "#fff"
      }
    ]
  };

  // 环形图配置
  const chartOptions = {
    cutout: "70%", // 空心部分大小
    plugins: {
      legend: {
        position: "bottom", // ✅ 图例放在下面
        labels: {
          color: "#0b572e",
          font: { size: 16, weight: "bold" }
        }
      },
      tooltip: { enabled: true }
    },
    maintainAspectRatio: false,
  };

  return (
    <div className="report-page">
      {/* Header */}
      <header className="report-header">
        <button className="back-btn" onClick={() => navigate("/")}>⟵ 返回</button>
        <div className="header-center">
          <img src="/image/jycollege-logo.jpeg" alt="logo" className="logo" />
          <h1 className="glow-text">微塑料分析报告</h1>
        </div>
      </header>

      <main className="report-grid">
        {/* 左：原始图 & 分析图 */}
        <section className="report-images glass-card">
          <h3>原始图像</h3>
          {inputImage ? (
            <img src={inputImage} alt="原图" className="report-img" />
          ) : (
            <p>未选择图片</p>
          )}
          <p className="img-label">输入图（无标注）</p>

          <h3>分析结果图</h3>
          {outputImage ? (
            <img src={outputImage} alt="结果图" className="report-img" />
          ) : (
            <p>正在生成结果图...</p>
          )}
          <p className="img-label">YOLO 检测结果</p>
        </section>

        {/* 中：统计数据 */}
        <section className="report-stat glass-card">
          <h3>统计数据</h3>
          {Object.keys(summary).length > 0 ? (
            <>
              {/* 文本统计 */}
              {Object.entries(summary).map(([cls, count]) => (
                <p key={cls} style={{ fontSize: "18px", fontWeight: "bold" }}>
                  <strong>{cls}：</strong> {count}
                </p>
              ))}

              {/* 环形图 + 动态总数 */}
              <div style={{
                position: "relative",
                width: "280px",
                height: "280px",
                margin: "20px auto"
              }}>
                <Doughnut data={chartData} options={chartOptions} />
                <div style={{
                  position: "absolute",
                  top: "50%",
                  left: "50%",
                  transform: "translate(-50%, -50%)",
                  fontSize: "22px",
                  fontWeight: "700",
                  color: "#0b572e",
                  textAlign: "center"
                }}>
                  总数<br />{animatedCount}
                </div>
              </div>
            </>
          ) : (
            <p>正在统计中...</p>
          )}
        </section>

        {/* 右：分析结论 */}
        <section className="report-analysis glass-card">
          <h3>分析结论</h3>
          <p>{conclusion}</p>
        </section>
      </main>
    </div>
  );
}