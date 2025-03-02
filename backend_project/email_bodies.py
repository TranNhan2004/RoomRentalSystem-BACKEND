def get_reset_password_email_body(reset_link: str): 
    return (f"""
        Kính gửi quý khách,<br /><br />

        Chúng tôi xin xác nhận rằng, yêu cầu đặt lại mật khẩu của quý khách đã được ghi nhận. Để tiến hành đặt lại mật khẩu, quý khách vui lòng bấm vào liên kết dưới đây:<br /><br />

        {reset_link}<br /><br />

        Nếu quý khách không yêu cầu đặt lại mật khẩu, vui lòng liên hệ email dưới đây để báo cáo sự cố:<br />
        roomrental.thn.ct201.resolve@gmail.com<br /><br />

        ----------------------------------------------------------------<br /><br />

        <b>LƯU Ý:</b> Đây là email tự động, vui lòng không trả lời lại email này.<br /><br />

        Trân trọng,<br />  
        <b>Room Rental Company</b>
    """)

    
def get_active_account_email_body(reset_link: str):
    return (f"""
        Kính gửi quý khách,<br /><br />

        Chúng tôi xin xác nhận rằng, quý khách đã tạo tài khoản với email này trên website của chúng tôi. Để kích hoạt tài khoản, quý khách vui lòng bấm vào liên kết sau đây:<br /><br />

        {reset_link}<br /><br />

        Nếu quý khách không phải là chủ nhân của tài khoản này, vui lòng liên hệ email dưới đây để báo cáo sự cố:<br />
        roomrental.thn.ct201.resolve@gmail.com<br /><br />

        ----------------------------------------------------------------<br /><br />

        <b>LƯU Ý:</b> Đây là email tự động, vui lòng không trả lời lại email này.<br /><br />

        Trân trọng,<br /> 
        <b>Room Rental Company</b>
    """)
    

def get_password_from_manager_register_email_body(temp_password: str):
    return (f"""
        Kính gửi quý khách,<br /><br />

        Chúng tôi xin xác nhận rằng, quý khách đã được đăng ký tài khoản bởi người quản lý. Bên dưới là mật khẩu tài khoản tạm thời của quý khách, vui lòng không tiết lộ cho bất kỳ ai:<br />

        <p style="font-size: 15pt"><b>{temp_password}</b></p>

        <b>Vui lòng đổi mật khẩu ngay sau khi đăng nhập để đảm bảo an toàn thông tin.</b><br /><br />

        Nếu quý khách không phải là chủ nhân của tài khoản này, vui lòng liên hệ email dưới đây để báo cáo sự cố:<br /><br />
        roomrental.thn.ct201.resolve@gmail.com<br /><br />

        ----------------------------------------------------------------<br /><br />

        <b>LƯU Ý:</b> Đây là email tự động, vui lòng không trả lời lại email này.<br /><br />

        Trân trọng,<br />  
        <b>Room Rental Company</b>
    """)