class AVL:
    def __init__(self,data = None):
        self.data = data
        self.left = AVL() if data is not None else None
        self.right = AVL() if data is not None else None
        self.height = 1 if data is not None else 0

    def is_empty(self):
        return self.data is None

    def get_height(self):
        return self.height

    def update_height(self):
        self.height  = max(self.left.get_height(), self.right.get_height()) + 1

    def get_balance_factor(self):
        return self.left.get_height() - self.right.get_height()

    def left_rotate(self):
        new_root = self.right
        self.right = new_root.left
        new_root.left = self
        self.update_height()
        new_root.update_height()
        return new_root

    def right_rotate(self):
        new_root = self.left
        self.left = new_root.right
        new_root.right = self
        self.update_height()
        new_root.update_height()
        return new_root

    def insert(self, data):
        if self.is_empty():
            self.data = data
            self.height = 1
            self.left = AVL()
            self.right = AVL()
            return self


        if data < self.data:
            if self.left is None:
                self.left = AVL(data)
            else:
                self.left = self.left.insert(data)
        else:
            if self.right is None:
                self.right = AVL(data)
            else:
                self.right = self.right.insert(data)


        self.update_height()
        return self.balance()

    def balance(self):

        balance = self.get_balance_factor()

        # left heavy
        if balance > 1:
            if self.left.get_balance_factor() < 0: #lr
                self.left = self.left.left_rotate()
            return self.right_rotate() #ll

        # right heavy
        if balance < -1:
            if self.right.get_balance_factor() > 0: # rl
                self.right = self.right.right_rotate()
            return self.left_rotate() #rr

        return self


    def find_min(self):
        current = self
        while current.left and not current.left.is_empty():
            current = current.left
        return current

    def remove(self, data):
        if self.is_empty():
            return None

        if data < self.data:
            self.left = self.left.remove(data)
        elif data > self.data:
            self.right = self.right.remove(data)
        else:

            if self.left.is_empty():
                return self.right
            elif self.right.is_empty():
                return self.left


            min_larger_node = self.right.find_min()
            self.data = min_larger_node.data
            self.right = self.right.remove(min_larger_node.data)

        self.update_height()

        return self.balance()




    def print_tree(self, level=0, space="      "):
        if self.right and not self.right.is_empty():
            self.right.print_tree(level + 1, space)

        print(space * level + str(self.data))
        if self.left and not self.left.is_empty():
            self.left.print_tree(level + 1, space)



def test_avl():
    tree = AVL()

    print("test 1 - rr rotate")
    tree = tree.insert(30)
    tree = tree.insert(40)
    tree = tree.insert(50)

    print("\ntree after test 1:")
    tree.print_tree()

    print('\n')

    print("test 2 - ll rotate")

    tree = tree.insert(20)
    tree = tree.insert(10)

    print("\ntree after test 2:")
    tree.print_tree()

    print('\n')

    print("test 3 - lr rotate")
    tree = tree.insert(45)
    tree = tree.insert(47)

    print("\ntree after test 3:")
    tree.print_tree()

    print("test 4- rl rotate")
    tree = tree.insert(35)
    tree = tree.insert(32)

    print("\ntree after test 4:")
    tree.print_tree()

    print("test 5 - delete 10 - rotation needed ")
    tree = tree.remove(10)

    print("\ntree after test 5:")
    tree.print_tree()

    print("test 6 - delete root 40 - rotation needed ")
    tree = tree.remove(40)

    print("\ntree after test 6:")
    tree.print_tree()


test_avl()
