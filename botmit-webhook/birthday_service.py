token = '55F87A13-2416-4D8E-8B42-903FC6C07DD5'


class BirthdayService:
    def get_list_birthday(self, com_code, user_id, orgid):
        # Goi toi service cua AMIS
        return [{"Name": "Nguyễn Văn A", "Gender": 1, "Age": "29", "DepartmentName": "testamis2",
                 "EmployeeId": "55F87A13-2416-4D8E-8B42-903FC6C071D5"}]

    def get_lasted_birthday_message(self, com_code, user_id, orgid):
        return 'chúc mừng sinh nhật em! Chúc em luôn mạnh khỏe, hạnh phúc và luôn thành công trong công việc.'
