# 《27版880参考答案》PDF 分卷

原件 `【PDF】27版880参考答案(1).pdf` 共 243,023,326 字节（232M），**超过 Gitee 单文件 100M 上限**，无法直接入库，因此拆成 3 个分卷提交，内容零缺失。

| 文件 | 大小 |
|---|---|
| `part.00` | 83,886,080 |
| `part.01` | 83,886,080 |
| `part.02` | 75,251,166 |
| 合计 | 243,023,326（与原件一致） |

`SHA256SUMS.txt` 是原件的 sha256，还原后脚本会自动比对。

## 还原

clone 或 pull 之后跑一次，PDF 会写回项目根目录（`302math/`）：

```bash
# Linux / macOS / Git Bash
bash assets/880-answers/restore.sh
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File .\assets\880-answers\restore.ps1
```

还原出的 PDF 本身被 `.gitignore` 排除，不会重复入库。

## 分卷是怎么生成的

```bash
split -b 80m -d '【PDF】27版880参考答案(1).pdf' assets/880-answers/part.
sha256sum '【PDF】27版880参考答案(1).pdf' > assets/880-answers/SHA256SUMS.txt
```

换了原件就照上面两条重新生成，并把旧的 `part.*` 删掉。
