import pandas as pd
from datetime import date
import json
data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"

class Account:
    def __init__(self, account_name, account_number):
        # Variable we used
        self.account_name = account_name
        self.account_number = account_number

    def Creat(self):
        # 呼叫檔案，利用CSV代替資料庫的使用，並透過檢查是否有已經存在的帳號名稱
        data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"
        df = pd.read_csv(data_path)# 從CSV抓出資料
        if self.account_name in df['Account_name'].values:#檢查是否有相同的資料
            print(f'{self.account_name} 已存在於 DataFrame 中，請選擇一個不同的名稱。')
            return True
        else:
            # 新增名稱
            new_data = {'Account_name': self.account_name,'Account_number': self.account_number}
            # 將舊df和新的df合併
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(data_path, index=False)  # 儲存到 CSV 檔案
            print(f'{self.account_name} 已成功新增到 DataFrame。')
            return False

    def Log_in(self):
        # data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"
        df = pd.read_csv(data_path)
        # 找出資料中符合的account_name，並檢查其account_number是否正確
        if self.account_name in df['Account_name'].values and self.account_number in df['Account_number'].values:
            print("Success!!")
            return False
        else:
            print("Error input!!")
            return True

    def Revise(self):
        self.Display()
        data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"
        df = pd.read_csv(data_path)
        while True:
            choice=input("1.What do you want to Revise?\n1.Account name.\n2.Account number.")
            if choice=="1":
                new_name=input("What's your new name?")
                if new_name.isalpha()==False:
                    print("Only can input English")
                # 更改名字
                else:
                    df.loc[df['Account_name'] == self.account_name, 'Account_name'] = new_name
                    df.to_csv(data_path, index=False)
                    self.account_name=new_name
                    return new_name
            elif choice=="2":
                new_number=input("What's your new number?")
                # 更改密碼
                df.loc[df['Account_name'] == self.account_name, 'Account_number'] = new_number    
                df.to_csv(data_path, index=False)
                self.account_number=new_number
                break
            else:
                print("Error")

    def Delete(self):
        # data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"
        df = pd.read_csv(data_path)
        choice=input("Are you sure to delete your account?[yes/no]")
        if choice.upper()=="YES":
            # 只留下不等於account_name的資料
            df = df[df['Account_name'] != self.account_name]
            df.to_csv(data_path, index=False)
            return False
        elif choice.upper()=="NO":
            return True
        else:
            print("Error")
            return True

    def Display(self):
        print("Account_name",self.account_name,"\nAccount_number",self.account_number)
# 以上目前不需修改




class Budget(Account):
    def __init__(self, account_name, account_number, balance, proportion, limit):
        super().__init__(account_name, account_number)
        # 不指定會出錯
        self.balance = float(balance)
        self.proportion = proportion
        self.limit=float(limit)

    def distribute(self):
        # list要先轉換成str，才能存到csv
        save_proportion = ','.join(str(num) for num in self.proportion)
        df = pd.read_csv(data_path)
        # 將 self.balance 的值赋给符合条件的行的 'Account_balance' 列
        df.loc[df['Account_name'] == self.account_name, 'Account_balance'] = self.balance
        df.loc[df['Account_name'] == self.account_name, 'Proportion'] = save_proportion
        df.loc[df['Account_name'] == self.account_name, 'Limit'] = self.limit
        category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
        # category="Food,Clothing,Living,Transportation,Education,Recreation"
        category = category.split(',')
        amount=[]
        for i in range(len(category)):
            # 要不要加limit??
            amount.append((int(self.proportion[i])/100)*self.balance)
        save_amount = ','.join(str(num) for num in amount)
        df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_amount
        df.to_csv(data_path, index=False)

    def Category(self):
        # data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"
        df = pd.read_csv(data_path)
        category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
        category = category.split(',')
        category.append(input("What do you want to add in the category?"))
        category =  ','.join(category)
        df.loc[df['Account_name'] == self.account_name, "Category"] = category
        df.to_csv(data_path, index=False)


    def Display(self):
        df = pd.read_csv(data_path)
        selected_category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
        selected_category=selected_category.split(',')
        selected_distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
        selected_distribute=selected_distribute.split(',')
        for i in range(len(selected_distribute)):
            print(selected_category[i],":",selected_distribute[i])

        
class Recording(Account):
    def __init__(self, account_name, account_number):
        super().__init__(account_name, account_number)
    
    def expenditure(self):
        df = pd.read_csv(data_path)
        df['Recording'] = df['Recording'].astype(str)
        recording = df.loc[df['Account_name'] == self.account_name, 'Recording'].values[0]
        while True:
            amount=input("How much do you expenditure")
            if amount.isdigit()==True:
                break
        balance=df.loc[df['Account_name'] == self.account_name, 'Account_balance'].values[0]
        balance=int(balance)-int(amount)
        limit = df.loc[df['Account_name'] == self.account_name, 'Limit'].values[0]
        if balance<int(limit)*(-1):
            print("You are bankruptcy, this expenditure can not success")
        else:
            explain=input("What do you by")
            while True:
                category=input("which category do you use")
                df = pd.read_csv(data_path)
                Category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
                Category = Category.split(',')
                if category in Category:
                    break
                else:
                    print("The category is not exist")
                    print("Your category is:",Category)
            Date= date.today()
            Date = str(Date)
            if recording != "nan":
                data_dict = json.loads(recording) # 因為這裡是從Series中取出字串，所以需要使用json.loads轉換成字典
                df_pushes = pd.DataFrame.from_dict(data_dict, orient='index')
                # 使用loc[]方法添加单个值或者一行数据
                if df_pushes.empty:
                    save = {"0":{"Amount": amount, "Explain": explain, "Category": category, "Date": Date}}
                    print(save)
                    data=[]
                    data.append(save)
                    data = json.dumps(data)
                    data = data[1:-1]
                    df['Recording'] = df['Recording'].astype(str)
                    df.loc[df['Account_name'] == self.account_name, "Recording"] = data
                    df.to_csv(data_path, index=False)
                else:
                    df_pushes.loc[len(df_pushes)] = [amount, explain, category, Date]  # 使用实际的值替换[value1, value2, ...]
                    pushes_json = df_pushes.to_json(orient='index', force_ascii=False)
                    df.loc[df['Account_name'] == self.account_name, "Recording"] = pushes_json
                    df.to_csv(data_path, index=False)
            else:
                # 使用loc[]方法添加单个值或者一行数据
                save = {"0":{"Amount": amount, "Explain": explain, "Category": category, "Date": Date}}
                print(save)
                data=[]
                data.append(save)
                data = json.dumps(data)
                data = data[1:-1]
                df['Recording'] = df['Recording'].astype(str)
                df.loc[df['Account_name'] == self.account_name, "Recording"] = data
                df.to_csv(data_path, index=False)
            df.loc[df['Account_name'] == self.account_name, "Account_balance"] = balance
            df.to_csv(data_path, index=False)
            Category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
            Category=Category.split(',')
            distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
            distribute=distribute.split(',')
            distribute[Category.index(category)]=float(distribute[Category.index(category)])-float(amount)
            distribute = ','.join(str(num) for num in distribute)
            df.loc[df['Account_name'] == self.account_name, "Distribute"] = distribute
            df.to_csv(data_path, index=False)

    def income(self):
        while True:
            amount=input("How much new income did you add?")
            if amount.isdigit()==True:
                break
        explain=input("Why did you get this money")
        category="Income"
        Date= date.today()
        Date = str(Date)
        # 抓出原始資料
        df = pd.read_csv(data_path)
        df['Recording'] = df['Recording'].astype(str)
        recording = df.loc[df['Account_name'] == self.account_name, 'Recording'].values[0]
        if recording != "nan":
            data_dict = json.loads(recording) # 因為這裡是從Series中取出字串，所以需要使用json.loads轉換成字典
            df_pushes = pd.DataFrame.from_dict(data_dict, orient='index')
            if df_pushes.empty:
                save = {"0":{"Amount": amount, "Explain": explain, "Category": category, "Date": Date}}
                print(save)
                data=[]
                data.append(save)
                data = json.dumps(data)
                data = data[1:-1]
                df.loc[df['Account_name'] == self.account_name, "Recording"] = data
                df['Recording'] = df['Recording'].astype(str)
                df.to_csv(data_path, index=False)
            # 使用loc[]方法添加单个值或者一行数据
            else:
                df_pushes.loc[len(df_pushes)] = [amount, explain, category, Date]  # 使用实际的值替换[value1, value2, ...]
                pushes_json = df_pushes.to_json(orient='index', force_ascii=False)
                df.loc[df['Account_name'] == self.account_name, "Recording"] = pushes_json
                df.to_csv(data_path, index=False)
        else:
            # 使用loc[]方法添加单个值或者一行数据
            save = {"0":{"Amount": amount, "Explain": explain, "Category": category, "Date": Date}}
            print(save)
            data=[]
            data.append(save)
            data = json.dumps(data)
            data = data[1:-1]
            df.loc[df['Account_name'] == self.account_name, "Recording"] = data
            df['Recording'] = df['Recording'].astype(str)
            df.to_csv(data_path, index=False)
        balance=df.loc[df['Account_name'] == self.account_name, 'Account_balance'].values[0]
        balance=int(balance)+int(amount)
        df.loc[df['Account_name'] == self.account_name, "Account_balance"] = balance
        df.to_csv(data_path, index=False)
        distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
        distribute=distribute.split(',')
        proportion = df.loc[df['Account_name'] == self.account_name, 'Proportion'].values[0]
        proportion=proportion.split(',')
        save_amount=[]
        for i in range(len(proportion)):
            save_amount.append((float(proportion[i])/100)*float(amount))
        distribute = [float(value) for value in distribute]
        result = [x + y for x, y in zip(distribute, save_amount)]
        save_result = ','.join(str(num) for num in result)
        df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_result
        df.to_csv(data_path, index=False)


    def Revise(self):
        df = pd.read_csv(data_path)
        recording = df.loc[df['Account_name'] == self.account_name, 'Recording'].values[0]
        data_dict = json.loads(recording) 
        df_pushes = pd.DataFrame.from_dict(data_dict, orient='index')
        limit = df.loc[df['Account_name'] == self.account_name, 'Limit'].values[0]
        index=input("Which transaction history do you want to revise")
        while True:
            if index in df_pushes.index:
                print(df_pushes.iloc[int(index)])
                choice=input("What do you want to revise?\n1.Amount\n2.Explain\n3.Category\n4.Go back")
                if choice=="1":
                    while True:
                        change=input("You want to change to?")
                        if change.isdigit()==True:
                            break
                    original_amount=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Amount')]
                    df_pushes.iloc[int(index), df_pushes.columns.get_loc('Amount')]=change
                    df_pushes.to_csv(data_path, index=False)
                    balance = df.loc[df['Account_name'] == self.account_name, 'Account_balance'].values[0]
                    if df_pushes.iloc[int(index)]['Category']!="Income":
                        balance=int(balance)+int(original_amount)-int(change)
                        print(balance)
                        if balance<int(limit)*(-1):
                            print("You are bankruptcy, this expenditure can not success")
                        else:
                            df.loc[df['Account_name'] == self.account_name, "Account_balance"] = balance
                            original_category=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Category')]
                            category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
                            category = category.split(',')
                            distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
                            distribute = distribute.split(',')
                            distribute[category.index(original_category)]=float(distribute[category.index(original_category)])+float(original_amount)-float(change)
                            save_distribute = ','.join(str(num) for num in distribute)
                            df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_distribute
                            df.to_csv(data_path, index=False)
                    else:
                        balance=int(balance)-int(original_amount)+int(change)
                        print(balance)
                        if balance<int(limit)*(-1):
                            print("You are bankruptcy, this expenditure can not success")
                        else:
                            df.loc[df['Account_name'] == self.account_name, "Account_balance"] = balance
                            distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
                            distribute = distribute.split(',')
                            proportion = df.loc[df['Account_name'] == self.account_name, 'Proportion'].values[0]
                            proportion = proportion.split(',')
                            original_category=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Category')]
                            amount=[]
                            for i in range(len(proportion)):
                                amount.append(((float(proportion[i]))/100)*(float(change)-float(original_amount)))
                            distribute = [float(value) for value in distribute]
                            result = [x + y for x, y in zip(distribute, amount)]
                            save_result = ','.join(str(num) for num in result)
                            df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_result
                            df.to_csv(data_path, index=False)

                elif choice=="2":
                    change=input("You want to change to?")
                    df_pushes.iloc[int(index), df_pushes.columns.get_loc('Explain')]=change
                    df_pushes.to_csv(data_path, index=False)
                elif choice=="3":
                    while True:
                        if df_pushes.iloc[int(index)]['Category']!="Income":
                            change=input("You want to change to?")
                            df = pd.read_csv(data_path)
                            Category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
                            Category = Category.split(',')
                            if change in Category:
                                original_category=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Category')]
                                amount=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Amount')]
                                df_pushes.iloc[int(index), df_pushes.columns.get_loc('Category')]=change
                                df_pushes.to_csv(data_path, index=False)
                                distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
                                distribute = distribute.split(',')
                                category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
                                category = category.split(',')
                                distribute[category.index(original_category)]=float(distribute[category.index(original_category)])+float(amount)
                                distribute[category.index(change)]=float(distribute[category.index(change)])-float(amount)
                                save_distribute = ','.join(str(num) for num in distribute)
                                df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_distribute
                                df.to_csv(data_path, index=False)
                                break
                            else:
                                print("The category is not exist")
                                print("Your category is:",Category) 
                        else:
                            print("You can't change the Income, please delete it.")
                            break
                elif choice=="4":
                    break
                else:
                    print("Error input")
            pushes_json = df_pushes.to_json(orient='index', force_ascii=False)
            df.loc[df['Account_name'] == self.account_name, "Recording"] = pushes_json
            df.to_csv(data_path, index=False)

    def Delete(self):
        df = pd.read_csv(data_path)
        recording = df.loc[df['Account_name'] == self.account_name, 'Recording'].values[0]
        data_dict = json.loads(recording) # 因為這裡是從Series中取出字串，所以需要使用json.loads轉換成字典
        df_pushes = pd.DataFrame.from_dict(data_dict, orient='index')
        limit = df.loc[df['Account_name'] == self.account_name, 'Limit'].values[0]
        index=input("Which transaction history do you want to delete?(If you don't have any history please entry any button to go back)")
        if index in df_pushes.index:
            print(df_pushes.iloc[int(index)])
            choice=input("Are you sure to delete it?[Yes/No]")
            if choice.upper()=="YES":
                if df_pushes.iloc[int(index)]['Category']!="Income":
                    original_amount=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Amount')]
                    original_category=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Category')]
                    category = df.loc[df['Account_name'] == self.account_name, 'Category'].values[0]
                    category = category.split(',')
                    distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
                    distribute = distribute.split(',')
                    distribute[category.index(original_category)]=float(distribute[category.index(original_category)])+float(original_amount)
                    save_distribute = ','.join(str(num) for num in distribute)
                    df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_distribute
                    balance = df.loc[df['Account_name'] == self.account_name, 'Account_balance'].values[0]
                    balance=int(balance)+int(original_amount)
                    if balance<int(limit)*(-1):
                        print("You are bankruptcy, this expenditure can not success")
                    else:
                        df.loc[df['Account_name'] == self.account_name, "Account_balance"] = balance
                        df.to_csv(data_path, index=False)
                        df_pushes = df_pushes.drop(index)
                        df_pushes = df_pushes.reset_index(drop=True)
                        print(df_pushes)
                        pushes_json = df_pushes.to_json(orient='index', force_ascii=False)
                        df.loc[df['Account_name'] == self.account_name, "Recording"] = pushes_json
                        df.to_csv(data_path, index=False)
                else:
                    original_amount=df_pushes.iloc[int(index), df_pushes.columns.get_loc('Amount')]
                    balance = df.loc[df['Account_name'] == self.account_name, 'Account_balance'].values[0]
                    balance=int(balance)-int(original_amount)
                    if balance<int(limit)*(-1):
                        print("You are bankruptcy, this expenditure can not success")
                    else:
                        df.loc[df['Account_name'] == self.account_name, "Account_balance"] = balance
                        proportion = df.loc[df['Account_name'] == self.account_name, 'Proportion'].values[0]
                        proportion = proportion.split(',')
                        distribute = df.loc[df['Account_name'] == self.account_name, 'Distribute'].values[0]
                        distribute = distribute.split(',')
                        amount=[]
                        for i in range(len(proportion)):
                            amount.append(((float(proportion[i]))/100)*(float(original_amount)))
                        distribute = [float(value) for value in distribute]
                        result = [x - y for x, y in zip(distribute, amount)]
                        save_result = ','.join(str(num) for num in result)
                        df.loc[df['Account_name'] == self.account_name, "Distribute"] = save_result
                        df.to_csv(data_path, index=False)
                        df_pushes = df_pushes.drop(index)
                        df_pushes = df_pushes.reset_index(drop=True)
                        print(df_pushes)
                        pushes_json = df_pushes.to_json(orient='index', force_ascii=False)
                        df.loc[df['Account_name'] == self.account_name, "Recording"] = pushes_json
                        df.to_csv(data_path, index=False)
            elif choice.upper()=="NO":
                pass
            else:
                print("Error")
        else:
            print("Error")



    def Display(self):
        df = pd.read_csv(data_path)
        df['Recording'] = df['Recording'].astype(str)
        recording = df.loc[df['Account_name'] == self.account_name, 'Recording'].values[0]
        if recording != "nan":
            data_dict = json.loads(recording) # 因為這裡是從Series中取出字串，所以需要使用json.loads轉換成字典
            df_pushes = pd.DataFrame.from_dict(data_dict, orient='index')
            print(df_pushes)
        else:
            print("You don't have any recording")



class Capability:
    def management(name,number):
        while True:
            # data_path = "C:\\Users\\ddwu0\\OneDrive\\桌面\\min_project\\Account_data.csv"
            df = pd.read_csv(data_path)
            balance = df.loc[df['Account_name'] == name, 'Account_balance'].values[0]
            limit = df.loc[df['Account_name'] == name, 'Limit'].values[0]
            Category = df.loc[df['Account_name'] == name, 'Category'].values[0]
            proportion = []
            budget = Budget(name,number,balance,proportion,limit)
            choice=input("1.Manage your money.\n2.display.\n3.Go back.")
            if choice=="1":
                choice1=input("1.distribute your money.\n2.New one category.")
                if choice1=="1":
                    proportion = []
                    Category = Category.split(',')
                    print("Your category is:",Category)
                    print("What do you want to distribute your money?(the total need to be 100)")
                    for i in range(len(Category)-1):
                        proportion.append(int(input(Category[i])))
                    if all(str(x).isdigit() for x in proportion)==True:
                        if sum(proportion)==100:
                            budget = Budget(name,number,balance,proportion,limit)
                            budget.distribute()
                            budget.Display()
                            break
                        else:
                            print("The total is not 100")
                    else:
                        print("Input must be positive int")
                elif choice1=="2":
                    budget.Category()
                    go=True
                    while go==True:
                        df = pd.read_csv(data_path)
                        balance = df.loc[df['Account_name'] == name, 'Account_balance'].values[0]
                        limit = df.loc[df['Account_name'] == name, 'Limit'].values[0]
                        Category = df.loc[df['Account_name'] == name, 'Category'].values[0]
                        proportion = []
                        Category = Category.split(',')
                        print("Your category is:",Category)
                        print("What do you want to distribute your money?(the total need to be 100)")
                        for i in range(len(Category)):
                            proportion.append(int(input(Category[i])))
                        if all(str(x).isdigit() for x in proportion)==True:
                            if sum(proportion)==100:
                                budget = Budget(name,number,balance,proportion,limit)
                                budget.distribute()
                                budget.Display()
                                break
                            else:
                                print("The total is not 100")
                        else:
                            print("Input must be positive int")
            elif choice=="2":
                budget.Display()
            elif choice=="3":
                break  
            else:
                print("error input")

    def first_time(name,number):
        while True:
            balance=input("How much do you have?")
            if balance.isdigit():   
                limit=input("What's your limit?")
                if limit.isdigit():
                    df = pd.read_csv(data_path)
                    df.loc[df['Account_name'] == name, "Category"] = "Food,Clothing,Living,Transportation,Education,Recreation"
                    df.to_csv(data_path, index=False)
                    proportion = []
                    proportion.append(input("What do you want to distribute your money for Food,Clothing,Living,Transportation,Education,Recreation?(the total need to be 100)\n1.Food"))
                    proportion.append(input("2.Clothing"))
                    proportion.append(input("3.Living"))
                    proportion.append(input("4.Transportation"))
                    proportion.append(input("5.Education"))
                    proportion.append(input("6.Recreation"))
                    if all(str(x).isdigit() for x in proportion)==True:
                        proportion = [int(x) for x in proportion]
                        if sum(proportion)==100:
                            budget = Budget(name,number,balance,proportion,limit)
                            budget.distribute()
                            budget.Display()
                            break
                        else:
                            print("The total is not 100")
                    else:
                        print("Input must be positive int")
                else:
                    print("Input must be positive int")
            else:
                print("Input must be positive int")

    def Record(name,number):
        while True:
            record=Recording(name,number)
            choice=input("1.Record transaction history.\n2.Display transaction history.\n3.Revise transaction history\n4.Delete transaction history\n5.GO back")
            if choice=="1":
                choice1=input("1.Icome.\n2.Expenditure.")
                if choice1=="1":
                    record.income()
                elif choice1=="2":
                    record.expenditure()
            elif choice=="2":
                record.Display()
            elif choice=="3":
                record.Display()
                record.Revise()
            elif choice=="4":
                record.Display()
                record.Delete()
            elif choice=="5":
                break
            else:
                print("Error input")

    def first():
        lock=True
        while lock==True:
            choice=input("1.Create a Account.\n2.Log in your Account.")
            if choice=="1" or choice=="2":
                name=input("Your account name.")
                if name.isalpha()==False:
                    print("Only can input English")
                else:
                    number=input("Your account number.")
                    account = Account(name,number)
                    if choice=="1":
                        lock1=account.Creat()
                        if lock1==False:
                            Capability.first_time(name,number)
                            lock=lock1
                    elif choice=="2":
                        lock=account.Log_in()
            else:
                print("Error")
        lock1=True
        while lock1==True:
            choice=input("1.Revise your Account information.\n2.Delete your Account.\n3.Display your Account detail.\n4.Manage your money.\n5.Recording your trade.\n6.Log out.")
            if choice=="1":
                new_name=account.Revise()
                name=new_name
            elif choice=="2":
                lock1=account.Delete()
            elif choice=="3":
                account.Display()
            elif choice=="4":
                Capability.management(name,number)
            elif choice=="5":
                Capability.Record(name,number)
            elif choice=="6":
                print("Bye~~")
                break
            else:
                print("error input")


if __name__ == "__main__":
    Capability.first()
