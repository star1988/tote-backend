class Student:

  
    def __init__ (self,name,marks):
        self.name = name
        self.marks = marks
    @staticmethod
    def Welcome():
        print("Welcome to Class")

    def get_avg(self):
        sum = 0
        for val in self.marks:
            sum += val
        print("Hi", self.name, "Your avarage marks are ", sum/3, "%")

    

s1 = Student("Mehmood", [97,98,99])
s1.get_avg()
s1.Welcome()

class Account:
    def __init__(self, balance, acc_no):
        self.balance = balance
        self.acc_no = acc_no

    def debit(self, amount):
        self.balance -= amount
        print("Rs", amount, "was debited from account no", self.acc_no )
        print("Total Balance = ", self.get_balance())

    def credit(self, amount):
        self.balance += amount
        print("Rs", amount, "was credited to account no", self.acc_no)
        print("Total Balance = ", self.get_balance())

    def get_balance(self):
        return self.balance
    
acc1 = Account(10000, 12345)
acc1.credit(3000)
acc1.debit(1500)

acc2 = Account(0,12346)
acc2.credit(9000)
acc2.debit(1000)

acc1.credit(30000)