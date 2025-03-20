# Anti Decompile Python v3

[![Phiên bản](https://img.shields.io/badge/Phiên%20bản-v3.0-blue.svg)](https://github.com/hoangturong/anti-decompile-v3/releases/tag/v3.0)

Ngăn chặn việc dịch ngược mã nguồn Python của bạn với Anti Decompile Python v3!

## Mô tả

Anti Decompile Python v3 là một công cụ mạnh mẽ giúp bảo vệ mã nguồn Python của bạn khỏi bị dịch ngược, đảm bảo an toàn cho tài sản trí tuệ của bạn. Bằng cách sử dụng các kỹ thuật mã hóa và che giấu, công cụ này làm cho việc phân tích và hiểu mã nguồn trở nên cực kỳ khó khăn, ngay cả đối với những người có kinh nghiệm.

## Tính năng

* **Bảo vệ mạnh mẽ**: Ngăn chặn hiệu quả các công cụ dịch ngược mã nguồn Python phổ biến.
* **Dễ sử dụng**: Tích hợp đơn giản vào dự án Python của bạn.
* **Tương thích**: Hoạt động với Python 3.x.
* **Tùy chỉnh**: Cho phép tùy chỉnh mức độ bảo vệ.
* **Tài liệu chi tiết**: Hướng dẫn rõ ràng và dễ hiểu.

## Cài đặt

1.  Sao chép kho lưu trữ:

    ```bash
    git clone [https://github.com/hoangturong/anti-decompile-v3.git](https://github.com/hoangturong/anti-decompile-v3.git)
    ```

2.  Cài đặt các phụ thuộc (nếu có):

    ```bash
    pip install -r requirements.txt
    ```

## Hướng dẫn sử dụng

1.  Nhập tệp `anti.py` vào tệp Python bạn muốn bảo vệ:

    ```python
    from anti import protect_main
    antii = protect_main()
    ```

2.  Thêm decorator `@antii` trước hàm `main()`:

    ```python
    @antii
    def main():
        print('Hello World')
        input('Nhấn Enter để thoát: ')

    if __name__ == "__main__":
        main()
    ```

3.  Cài đặt `auto-py-to-exe`:

    ```bash
    pip install auto-py-to-exe
    ```

4.  Chạy `auto-py-to-exe`:

    ```bash
    auto-py-to-exe
    ```

    * Xem hướng dẫn sử dụng `auto-py-to-exe` [Tại đây.](https://pypi.org/project/auto-py-to-exe/)

5.  Biên dịch thành tệp thực thi (.exe) và kiểm tra.

    * Thành công!

## Đóng góp

Chào mừng mọi đóng góp!.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc đề xuất nào, vui lòng liên hệ với tôi qua email: [trong20843@gmail.com](mailto:trong20843@gmail.com)

## Lời cảm ơn

Xin cảm ơn tất cả những người đã đóng góp vào dự án này!
