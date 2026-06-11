# SHA256SUMS 文件生成说明

## 概述
`SHA256SUMS` 文件包含了 `stack.py` 文件的SHA256哈希值，用于验证文件的完整性和真实性。这是一种常见的软件发布实践，确保文件在传输或存储过程中未被篡改。

## 生成过程
`SHA256SUMS` 文件是通过以下步骤生成的：

1. **计算哈希值**：
   - 使用PowerShell命令 `Get-FileHash` 计算 `stack.py` 的SHA256哈希值。
   - 命令：`Get-FileHash -Algorithm SHA256 -Path "c:\Users\wang7\Desktop\新建文件夹\repo\suanfa\stack.py"`
   - 输出哈希值：`DEBDC08052F46CC3BAD15F82EC496C81A0310ADDFC24C19BD2D0E9AE329B85C6`

2. **创建校验文件**：
   - 将哈希值和文件名格式化为标准SHA256SUMS格式：`哈希值 *文件名`
   - 内容：`DEBDC08052F46CC3BAD15F82EC496C81A0310ADDFC24C19BD2D0E9AE329B85C6 *stack.py`
   - 保存为 `SHA256SUMS` 文件。

## 验证方法
要验证文件是否正确，使用以下命令：
- PowerShell：`Get-FileHash -Algorithm SHA256 -Path "stack.py"` 并比较哈希值。
- Linux/Unix：`sha256sum -c SHA256SUMS`

如果哈希值匹配，文件完整；否则，文件可能已被修改。

