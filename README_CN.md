# 命令行文件内容保存器

## 概述

命令行文件内容保存器是一个 Python 脚本，旨在递归遍历指定文件夹，并将符合条件的文件内容保存到一个 JSON 文件中。该脚本用于传入ChatGPT提问。

该脚本支持自定义需要包含的文件类型，并为输出的 JSON 文件自动生成元数据，包括项目信息和从 README 文件中提取的描述（如果存在）。

## 功能特点

- 递归遍历文件夹，保存指定类型文件的内容。
- 支持自定义文件扩展名来决定包含哪些文件。
- 包含项目的元数据信息，包括创建时间、版本以及从 README.md 或 README 文件中提取的描述。
- 支持多种字符集的编码处理，尝试使用常见编码来解码文件内容。
- 显示处理过程中最大的几个文件的相关信息，方便快速了解项目的情况。

## 前提条件

- Python 3.x

您可能需要安装 `chardet` 库，以确保脚本能够正确处理各种编码。

```sh
pip install chardet
```

## 使用说明

### 命令行参数

该脚本使用命令行参数来指定要处理的文件夹和所需的输出格式。以下是可用的命令行参数：

- `folder_path`（必需）：要保存文件的文件夹路径。
- `file_extensions`（可选）：要包含的文件扩展名列表。如果未指定，默认保存 `.py` 文件。
- `-o` 或 `--output`（可选）：输出 JSON 文件的路径。如果未提供，则在指定文件夹中创建一个带有时间戳名称的 JSON 文件。

### 示例用法

运行脚本并仅保存 Python 文件（`.py`）：

```sh
python script.py /path/to/folder .py
```

运行脚本，包含 `.txt` 和 `.log` 文件，并指定输出文件：

```sh
python script.py /path/to/folder .txt .log -o /path/to/output/content.json
```

### 输出

- 输出保存在一个 JSON 文件中，该文件包含每个文件的内容，并通过相对路径进行标识。
- 输出的元数据包括：
  - **file_name**：输出 JSON 文件的名称。
  - **project_name**：项目文件夹的名称。
  - **creation_time**：JSON 文件的创建时间。
  - **version**：脚本的版本（默认为 `1.0`）。
  - **description**：从 README.md 或 README 文件中的第一行非空内容提取的描述。
  - **file_size**：生成的 JSON 文件的大小（可读格式）。
- 脚本还会显示处理过程中最大的文件列表，以内容大小进行排序。

## 错误处理

该脚本包含了健壮的错误处理机制，确保用户有流畅的体验：

- 处理文件夹或文件缺失的 `FileNotFoundError`。
- 处理文件夹或文件访问受限的 `PermissionError`。
- 使用多种编码尝试（`utf-8`, `gb2312`, `gbk` 等）来处理不同编码的文件。
- 对于空的 README 文件或不存在的 README 文件能优雅地处理。

## 示例

### 将 Python 文件保存到默认输出

```sh
python script.py /project/folder
```
该命令会将 `/project/folder` 中所有 `.py` 文件的内容保存到以时间戳命名的 JSON 文件中，存放在 `/project/folder` 目录下。

### 保存多种文件类型并指定输出路径

```sh
python script.py /project/folder .txt .log -o /project/folder/output_content.json
```
该命令会将 `/project/folder` 中的所有 `.txt` 和 `.log` 文件的内容保存到 `/project/folder/output_content.json` 中。

## 重要说明

- **README 提取**：如果文件夹中包含 `README.md` 或 `README` 文件，则会使用该文件中的第一行非空内容作为元数据中的描述。
- **文件大小显示**：保存 JSON 后，脚本会输出生成文件的大小，并显示最大的几个文件的信息。
- **编码处理**：脚本会尝试使用多种编码来解码文件，以确保兼容不同的文本格式。如果解码失败，文件将以二进制形式保存为十六进制字符串。

## 已知限制

- 如果文件无法解码，则会以十六进制字符串形式保存，这可能不易阅读。
- 对于包含大量文件的大型文件夹，由于递归遍历的特性，可能会导致性能瓶颈。
- 生成的 JSON 文件可能会很大，具体取决于文件数量和大小，因此请确保有足够的磁盘空间。

## 许可证

该脚本采用 MIT 许可证，您可以自由使用、修改和分发。

## 贡献

欢迎提交 issue 或通过提交 pull request 为项目做出贡献。欢迎所有贡献！

