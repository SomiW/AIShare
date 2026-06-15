# AI 开源工具志

AI 开源工具志是一份按开发场景整理的中文工具清单。站点使用纯 HTML
和 CSS，不需要构建步骤，可直接部署到 GitHub Pages。

## 本地预览

在仓库根目录启动 Python 静态服务器：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000`。

## 部署到 GitHub Pages

仓库包含 `.github/workflows/pages.yml`。完成以下设置后，每次推送到
`main` 或 `master` 分支都会自动部署：

1. 打开 GitHub 仓库的 **Settings > Pages**。
2. 在 **Build and deployment** 的 **Source** 中选择
   **GitHub Actions**。
3. 推送一次代码，或手动运行 **Deploy static site to Pages** 工作流。

## 收录标准

清单优先收录满足以下条件的项目：

- 有明确、可访问的官方代码仓库。
- 使用清晰的开源许可证。
- 解决具体开发问题，而不只是概念演示。
- 仍在维护，或具备稳定且持续的社区价值。

新增项目时，请提供项目用途、官方仓库、许可证、适用人群和推荐理由。
许可证信息仅用于快速参考，采用前请以项目仓库中的原始文件为准。

## 文件结构

- `index.html`：页面结构和工具内容。
- `styles.css`：视觉样式与响应式布局。
- `assets/`：页面插画。
- `tests/test_site.py`：静态结构与部署配置测试。
- `.github/workflows/pages.yml`：GitHub Pages 部署工作流。

## 许可证

本站代码使用 [MIT License](LICENSE)。各收录项目使用自己的许可证。
