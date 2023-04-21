import cv2
import numpy as np

"""
Hàm này nhận đầu vào là một hình ảnh và kích thước đích (mặc định là 80x80). Hàm này sẽ thực hiện việc thay đổi kích thước hình ảnh, chuyển đổi hình ảnh từ màu sang đen trắng, 
và áp dụng ngưỡng nhị phân. Hàm trả về hình ảnh đã được tiền xử lý.
"""
def preprocess_image(image, target_size=(80, 80)):
    resized_image = cv2.resize(image, target_size)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    return threshold_image

"""
Hàm này dùng để lưu thông tin huấn luyện vào các tệp văn bản và lưu hình ảnh vào đĩa. Hàm này sẽ thực hiện việc ghi thông tin về giá trị readout và giá trị lớp ẩn vào các tệp tương ứng, 
cũng như lưu hình ảnh vào thư mục chỉ định (mặc định là "logs").
"""
def save_logs(t, readout_t, h_fc1, s_t, x_t1, output_dir="logs"):
    if t % 10000 <= 100:
        readout_file = open(f"{output_dir}/readout.txt", 'a')
        hidden_file = open(f"{output_dir}/hidden.txt", 'a')
        
        readout_file.write(",".join([str(x) for x in readout_t]) + '\n')
        hidden_file.write(",".join([str(x) for x in h_fc1.eval(feed_dict={s: [s_t]})[0]]) + '\n')
        
        cv2.imwrite(f"{output_dir}/frame{t}.png", x_t1)
        
        readout_file.close()
        hidden_file.close()
