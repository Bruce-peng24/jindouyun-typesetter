# Pandoc-GUI 打包说明

## 打包方法

1. 确保 pandoc.exe 文件位于 pandoc 文件夹中
   - 如果文件缺失，可以从 pandoc.zip 解压恢复

2. 运行 `rebuild_app.bat` 脚本进行打包
   - 该脚本使用 Pandoc-GUI.spec 配置文件
   - 包含了所有必要的依赖和资源文件

3. 打包后的 exe 文件将位于 dist 文件夹中

## 注意事项

- 不要使用其他打包脚本，它们可能会缺少必要的配置
- Pandoc-GUI.spec 已正确配置所有必要的数据和依赖项
- 如果遇到问题，请检查 pandoc 文件夹中是否有 pandoc.exe 文件

## 故障排除

如果打包后的 exe 提示找不到 pandoc.exe：
1. 确认打包前 pandoc 文件夹中有 pandoc.exe
2. 确认没有使用错误的打包脚本
3. 删除 build 和 dist 文件夹后重新打包