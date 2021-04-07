import re
import pandas as pd

pattern_phil = "Phil\w*"
pattern_address = "(\w*)@"
pattern_provider = "@(\w*)"
pattern_multi_domain = "@\w*\.(\w+\.\w*)"
pattern_domain = "\.(\w*)"
pattern_width = "(?:com/(\d*))"
pattern_height = "(?:\d*x(\d*))"
pattern_img_extension = "(?:x\d*\.(\w*))"
ip_pattern = "\d{3}"
pattern_currency = "(^.)"
pattern_amount = "(?:^.)(\d*.*)"
pattern_exclude_chars = "[a-z]|[A-Z]"
pattern_pwd_char = "^\D+"
pattern_multilevel = "\.\w+\."


def file_read():
    data = pd.read_csv("personal_data.csv", encoding="UTF-8", delimiter=',')
    return data


def fileter_phil(data, pattern):
    names = list(data["first_name"].apply(str))
    filtered_names = []
    for name in names:
        filtered_name = re.search(pattern, name)
        if not (filtered_name is None):
            filtered_names.append(filtered_name.group())
    print("List of names containing Phil: " + str(filtered_names))


def regex_data(data, input_col_name, pattern, output_col_name):
    regex_data_list = list(data[input_col_name].apply(str))
    filtered_data_list = []
    for re_data in regex_data_list:
        filtered_data = re.search(pattern, re_data)
        filtered_data_list.append(filtered_data.group(1))
    data[output_col_name] = filtered_data_list
    print(data)


def regex_data_multi(data, input_col_name, pattern, output_col_name, pattern_multi):
    regex_data_list = list(data[input_col_name].apply(str))
    filtered_data_list = []
    for re_data in regex_data_list:
        filtered_data_multi = re.search(pattern_multi, re_data)
        if re.search(pattern_multi, re_data):
            filtered_data_list.append(filtered_data_multi.group(1))
        else:
            filtered_data_multi = re.search(pattern, re_data)
            filtered_data_list.append(filtered_data_multi.group(1))
    data[output_col_name] = filtered_data_list
    print(data)


def flag_is_hungarian(data):
    phone_num_list = list(data["phone_num"].apply(str))
    flag_list = []
    for num in phone_num_list:
        if num.startswith(("36", "06")):
            flag_list.append("true")
        else:
            flag_list.append("false")
    data.insert(loc=5, column="is_hu_phone", value=flag_list)
    print("Is Hungarian?\n" + str(data["is_hu_phone"]))


def ip_bigger(data, pattern):
    ips = list(data["ip_address"].apply(str))
    three_digit_ips = []
    for ip in ips:
        filtered_ip = list(map(int, re.findall(pattern, ip)))
        three_digit_ips.append(filtered_ip)
    three_digit_ips_list = [item for sublist in three_digit_ips for item in sublist]
    big_three_digit_ips_list = []
    for ip in three_digit_ips_list:
        if ip > 100:
            big_three_digit_ips_list.append(ip)
    print("Number of blocks: " + str(len(three_digit_ips_list)))
    print("Number of blocks bigger than 100: " + str(len(big_three_digit_ips_list)))


def flag_is_multilevel(data, pattern):
    emails = list(data["email"].apply(str))
    multilevel_emails = []
    for email in emails:
        if re.search(pattern, email):
            multilevel_emails.append("true")
        else:
            multilevel_emails.append("false")
    data.insert(loc=4, column="is_multilevel", value=multilevel_emails)
    print("Is multilevel?\n" + str(data["is_multilevel"]))


def personal_code_making(data, pattern):
    codes = list(data["personal_code"].apply(str))
    valid_codes = []
    ten_digit_codes = []
    for code in codes:
        valid_code = re.sub(pattern, "", code)
        valid_codes.append(valid_code)
    for digit_code in valid_codes:
        digit_code_zero = digit_code + str("0000000000000000000")
        if len(digit_code_zero) > 10:
            ten_digits = digit_code[:10]
            ten_digit_codes.append(ten_digits)
    data["personal_code"] = ten_digit_codes
    print("Personal codes:\n" + str(data["personal_code"]))


def phone_pwd_char_checker(data, pattern):
    phone_pwds = list(data["phone_password"].apply(str))
    filtered_data_list = []
    for pwd in phone_pwds:
        if re.match(pattern, pwd):
            filtered_data_list.append(pwd)
    print("Passwords containing characters: " + str(filtered_data_list))
    print("Number of passwords containing characters: " + str(len(filtered_data_list)))


def main():
    input_file = file_read()
    fileter_phil(input_file, pattern_phil)
    regex_data(input_file, "email", pattern_address, "address")
    regex_data(input_file, "email", pattern_provider, "provider")
    regex_data_multi(input_file, "email", pattern_domain, "domain", pattern_multi_domain)
    flag_is_hungarian(input_file)
    regex_data(input_file, "img_url", pattern_width, "width")
    regex_data(input_file, "img_url", pattern_height, "height")
    regex_data(input_file, "img_url", pattern_img_extension, "img_extension")
    ip_bigger(input_file, ip_pattern)
    flag_is_multilevel(input_file, pattern_multilevel)
    regex_data(input_file, "bank_account_amount", pattern_amount, "amount")
    regex_data(input_file, "bank_account_amount", pattern_currency, "currency")
    personal_code_making(input_file, pattern_exclude_chars)
    phone_pwd_char_checker(input_file, pattern_pwd_char)


main()
