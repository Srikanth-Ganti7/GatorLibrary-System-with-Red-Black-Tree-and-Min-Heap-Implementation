#Version 4.3 Working ADS project 1
#findClosest fixed
#Color flip not working

import sys
import time

class RedBlackTreeNode:
    def __init__(self, bookID, bookName, authorName, availabilityStatus, borrowedBy):
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus  # True if available, False otherwise
        self.borrowedBy = borrowedBy  # Patron ID who borrowed the book
        self.reservationHeap = None  # This will be a Binary Min-Heap instance
        

        # Red-Black Tree specific properties
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # Red = 1, Black = 0

        #Binary Min Heap for reservations
        self.reservationHeap = BinaryMinHeap()
    

    def __repr__(self):
        return f"BookID: {self.bookID}, Title: {self.bookName}, Author: {self.authorName}, Available: {self.availabilityStatus}, BorrowedBy: {self.borrowedBy}"

class RedBlackTree:
    def __init__(self, output_file):
        self.nilNode = RedBlackTreeNode(0, "", "", True, None)
        self.nilNode.color = 0  # Black
        self.nilNode.left = self.nilNode
        self.nilNode.right = self.nilNode
        self.root = self.nilNode
        self.colorFlipCount = 0
        self.output_file = output_file

    def write_to_file(self, content):
        with open(self.output_file, "a") as file:
            file.write(content + "\n")


    def _rotate_left(self, pivotNode):
        rightChild = pivotNode.right
        pivotNode.right = rightChild.left
        if rightChild.left != self.nilNode:
            rightChild.left.parent = pivotNode

        rightChild.parent = pivotNode.parent
        if pivotNode.parent is None:
            self.root = rightChild
        elif pivotNode == pivotNode.parent.left:
            pivotNode.parent.left = rightChild
        else:
            pivotNode.parent.right = rightChild
        rightChild.left = pivotNode
        pivotNode.parent = rightChild

    def _rotate_right(self, pivotNode):
        leftChild = pivotNode.left
        pivotNode.left = leftChild.right
        if leftChild.right != self.nilNode:
            leftChild.right.parent = pivotNode

        leftChild.parent = pivotNode.parent
        if pivotNode.parent is None:
            self.root = leftChild
        elif pivotNode == pivotNode.parent.right:
            pivotNode.parent.right = leftChild
        else:
            pivotNode.parent.left = leftChild
        leftChild.right = pivotNode
        pivotNode.parent = leftChild

    def Increment_color_flip(self, node, new_color):
        if node.color != new_color:
            self.colorFlipCount += 1
            node.color = new_color

    def adjustTreeInsert(self, newNode):
        while newNode.parent.color == 1:  # Red
            if newNode.parent == newNode.parent.parent.right:
                uncleNode = newNode.parent.parent.left
                if uncleNode.color == 1:  # Red
                    # Increment the color flip count for uncleNode, parent, and grandparent if needed
                    self.Increment_color_flip(uncleNode, 0)  # Black
                    self.Increment_color_flip(newNode.parent, 0)  # Black
                    self.Increment_color_flip(newNode.parent.parent, 1)  # Red
                    newNode = newNode.parent.parent
                else:
                    if newNode == newNode.parent.left:
                        newNode = newNode.parent
                        self._rotate_right(newNode)
                    # Increment the color flip count for parent and grandparent if needed
                    self.Increment_color_flip(newNode.parent, 0)  # Black
                    self.Increment_color_flip(newNode.parent.parent, 1)  # Red
                    self._rotate_left(newNode.parent.parent)
            else:
                uncleNode = newNode.parent.parent.right
                if uncleNode.color == 1:  # Red
                    # Increment the color flip count for uncleNode, parent, and grandparent if needed
                    self.Increment_color_flip(uncleNode, 0)  # Black
                    self.Increment_color_flip(newNode.parent, 0)  # Black
                    self.Increment_color_flip(newNode.parent.parent, 1)  # Red
                    newNode = newNode.parent.parent
                else:
                    if newNode == newNode.parent.right:
                        newNode = newNode.parent
                        self._rotate_left(newNode)
                    # Increment the color flip count for parent and grandparent if needed
                    self.Increment_color_flip(newNode.parent, 0)  # Black
                    self.Increment_color_flip(newNode.parent.parent, 1)  # Red
                    self._rotate_right(newNode.parent.parent)
            if newNode == self.root:
                break
        # Ensure the root is always black without incrementing the flip count
        if self.root.color != 0:
            self.root.color = 0

    def insert(self, bookID, bookName, authorName, availabilityStatus, borrowedBy):
        newNode = RedBlackTreeNode(bookID, bookName, authorName, availabilityStatus, borrowedBy)
        newNode.parent = None
        newNode.left = self.nilNode
        newNode.right = self.nilNode
        newNode.color = 1  # Red

        parentNode = None
        currentNode = self.root

        while currentNode != self.nilNode:
            parentNode = currentNode
            if newNode.bookID < currentNode.bookID:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right

        newNode.parent = parentNode
        if parentNode is None:
            self.root = newNode
        elif newNode.bookID < parentNode.bookID:
            parentNode.left = newNode
        else:
            parentNode.right = newNode

        if newNode.parent is None:
            newNode.color = 0
            return

        if newNode.parent.parent is None:
            return

        self.adjustTreeInsert(newNode)

    def get_color_flip_count(self):
        return self.colorFlipCount
    
    def search(self, bookID):
        return self._search_tree_helper(self.root, bookID)

    def _search_tree_helper(self, node, key):
        if node == self.nilNode or key == node.bookID:
            return node

        if key < node.bookID:
            return self._search_tree_helper(node.left, key)
        return self._search_tree_helper(node.right, key)

    # Additional method to delete a node - Simplified version
    def delete_node(self, bookID):
        self._delete_node_helper(self.root, bookID)

    def _delete_node_helper(self, node, key):
        targetNode = self.nilNode
        while node != self.nilNode:
            if node.bookID == key:
                targetNode = node

            if node.bookID <= key:
                node = node.right
            else:
                node = node.left

        if targetNode == self.nilNode:
            self.write_to_file("Node to be deleted not found")
            return

        replacementNode = targetNode
        originalColorOfReplacement = replacementNode.color
        if targetNode.left == self.nilNode:
            fixNode = targetNode.right
            self._rb_transplant(targetNode, targetNode.right)
        elif targetNode.right == self.nilNode:
            fixNode = targetNode.left
            self._rb_transplant(targetNode, targetNode.left)
        else:
            replacementNode = self._minimum(targetNode.right)
            originalColorOfReplacement = replacementNode.color
            fixNode = replacementNode.right
            if replacementNode.parent == targetNode:
                fixNode.parent = replacementNode
            else:
                self._rb_transplant(replacementNode, replacementNode.right)
                replacementNode.right = targetNode.right
                replacementNode.right.parent = replacementNode

            self._rb_transplant(targetNode, replacementNode)
            replacementNode.left = targetNode.left
            replacementNode.left.parent = replacementNode
            replacementNode.color = targetNode.color

        if originalColorOfReplacement == 0:
            self.adjustTreeDelete(fixNode)

    def _rb_transplant(self, sourceNode, replacementSubtree):
        if sourceNode.parent == None:
            self.root = replacementSubtree
        elif sourceNode == sourceNode.parent.left:
            sourceNode.parent.left = replacementSubtree
        else:
            sourceNode.parent.right = replacementSubtree
        if replacementSubtree:
            replacementSubtree.parent = sourceNode.parent

    def _minimum(self, node):
        while node.left != self.nilNode:
            node = node.left
        return node

    def adjustTreeDelete(self, fixNode):
        while fixNode != self.root and fixNode.color == 0:
            if fixNode == fixNode.parent.left:
                siblingNode = fixNode.parent.right
                if siblingNode.color == 1:
                    self.Increment_color_flip(siblingNode, 0)
                    self.Increment_color_flip(fixNode.parent, 1)
                    self._rotate_left(fixNode.parent)
                    siblingNode = fixNode.parent.right

                if siblingNode.left.color == 0 and siblingNode.right.color == 0:
                    self.Increment_color_flip(siblingNode, 1)
                    fixNode = fixNode.parent
                else:
                    if siblingNode.right.color == 0:
                        self.Increment_color_flip(siblingNode.left, 0)
                        self.Increment_color_flip(siblingNode, 1)
                        self._rotate_right(siblingNode)
                        siblingNode = fixNode.parent.right

                    self.Increment_color_flip(siblingNode, fixNode.parent.color)
                    self.Increment_color_flip(fixNode.parent, 0)
                    self.Increment_color_flip(siblingNode.right, 0)
                    self._rotate_left(fixNode.parent)
                    fixNode = self.root
            else:
                siblingNode = fixNode.parent.left
                if siblingNode.color == 1:
                    self.Increment_color_flip(siblingNode, 0)
                    self.Increment_color_flip(fixNode.parent, 1)
                    self._rotate_right(fixNode.parent)
                    siblingNode = fixNode.parent.left

                if siblingNode.right.color == 0 and siblingNode.left.color == 0:
                    self.Increment_color_flip(siblingNode, 1)
                    fixNode = fixNode.parent
                else:
                    if siblingNode.left.color == 0:
                        self.Increment_color_flip(siblingNode.right, 0)
                        self.Increment_color_flip(siblingNode, 1)
                        self._rotate_left(siblingNode)
                        siblingNode = fixNode.parent.left

                    self.Increment_color_flip(siblingNode, fixNode.parent.color)
                    self.Increment_color_flip(fixNode.parent, 0)
                    self.Increment_color_flip(siblingNode.left, 0)
                    self._rotate_right(fixNode.parent)
                    fixNode = self.root
        self.Increment_color_flip(fixNode, 0)

    # Method to print the tree content
    # def print_level_order(self):
    #     if self.root == self.nilNode:
    #         return

    #     queue = [self.root]
    #     output = []
    #     while len(queue) > 0:
    #         current = queue.pop(0)
    #         output.append(f'{current.bookID} ({current.bookName})', end=" ")

    #         if current.left != self.nilNode:
    #             queue.append(current.left)
    #         if current.right != self.nilNode:
    #             queue.append(current.right)
    #     self.write_to_file("".join(output))

    # def add_reservation(self, bookID, patronID, priorityNumber):
    #     bookNode = self.search(bookID)
    #     if bookNode != self.nilNode:
    #         reservation = HeapNode(patronID, priorityNumber)
    #         bookNode.reservationHeap.insert(reservation)
    #     else:
    #         self.write_to_file(f"Book with ID {bookID} not found.")

    # def allocate_book_to_next_patron(self, bookID):
    #     bookNode = self.search(bookID)
    #     if bookNode != self.nilNode and not bookNode.reservationHeap.is_empty():
    #         nextReservation = bookNode.reservationHeap.extract_min()
    #         bookNode.borrowedBy = nextReservation.patronID
    #         bookNode.availabilityStatus = False  # Book is now borrowed
    #         self.write_to_file(f"Book {bookID} allocated to Patron {nextReservation.patronID}.")
    #     else:
    #         self.write_to_file(f"No reservations found for Book {bookID}, or book not found.")
    #         bookNode.availabilityStatus = True  # Book is now available

class HeapNode:
    def __init__(self, patronID, priorityNumber, timeOfReservation=None):
        self.patronID = patronID
        self.priorityNumber = priorityNumber
        self.timeOfReservation = timeOfReservation if timeOfReservation is not None else time.time()

    def __lt__(self, other):
        if self.priorityNumber == other.priorityNumber:
            return self.timeOfReservation < other.timeOfReservation
        return self.priorityNumber < other.priorityNumber

    def __eq__(self, other):
        return self.priorityNumber == other.priorityNumber and self.timeOfReservation == other.timeOfReservation

    def __repr__(self):
        return f'HeapNode(PatronID: {self.patronID}, Priority: {self.priorityNumber}, TimeOfReservation: {self.timeOfReservation})'


#Binary Min Heap for reservations
class BinaryMinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, patronID, priorityNumber, timeOfReservation=None):
        heapNode = HeapNode(patronID, priorityNumber, timeOfReservation)
        self.heap.append(heapNode)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self):
        if self.is_empty():
            return None

        minimum = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._sift_down(0)
        return minimum

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent] > self.heap[index]:
                self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
                index = parent
            else:
                break

    def _sift_down(self, index):
        size = len(self.heap)
        while index < size:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left

            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def is_empty(self):
        return len(self.heap) == 0

    def peek(self):
        return self.heap[0] if not self.is_empty() else None

    def __repr__(self):
        return f"MinHeap: {self.heap}"






class LibrarySystem:
    def __init__(self, output_file):
        self.bookTree = RedBlackTree(output_file=output_file)
        self.output_file = output_file

        with open(self.output_file, 'w') as file:
            pass

    def write_to_file(self, content):
        with open(self.output_file, "a") as file:
            file.write(content + "\n")

    def print_book(self, bookID):
        bookNode = self.bookTree.search(bookID)
        if bookNode != self.bookTree.nilNode:
            availability = "Yes" if bookNode.availabilityStatus else "No"
            borrowedBy = bookNode.borrowedBy if bookNode.borrowedBy else "None"
            reservations = [reservation.patronID for reservation in bookNode.reservationHeap.heap]
            self.write_to_file(f"BookID = {bookNode.bookID}\nTitle = \"{bookNode.bookName}\"\nAuthor = \"{bookNode.authorName}\"\nAvailability = \"{availability}\"\nBorrowedBy = {borrowedBy}\nReservations = {reservations}")
        else:
            self.write_to_file(f"Book {bookID} not found in the Library")

    def print_books(self, bookID1, bookID2):
        # This requires an in-order traversal from bookID1 to bookID2
        self._print_books_helper(self.bookTree.root, bookID1, bookID2)

    def _print_books_helper(self, node, bookID1, bookID2):
        if node == self.bookTree.nilNode:
            return
        if bookID1 < node.bookID:
            self._print_books_helper(node.left, bookID1, bookID2)
        if bookID1 <= node.bookID <= bookID2:
            self._print_book_details(node)  # Call a method that prints the book details in the desired format.
        if bookID2 > node.bookID:
            self._print_books_helper(node.right, bookID1, bookID2)

    def _print_book_details(self, bookNode):
        availability = "Yes" if bookNode.availabilityStatus else "No"
        borrowedBy = bookNode.borrowedBy if bookNode.borrowedBy else "None"
        reservations = [r.patronID for r in bookNode.reservationHeap.heap]
        self.write_to_file(f"BookID = {bookNode.bookID}\nTitle = \"{bookNode.bookName}\"\nAuthor = \"{bookNode.authorName}\"\nAvailability = \"{availability}\"\nBorrowedBy = {borrowedBy}\nReservations = {reservations}")

    def insert_book(self, bookID, bookName, authorName, availabilityStatus, borrowedBy):
        self.bookTree.insert(bookID, bookName, authorName, availabilityStatus, borrowedBy)

    def borrow_book(self, patronID, bookID, patronPriority):
        bookNode = self.bookTree.search(bookID)
        if bookNode != self.bookTree.nilNode:
            if bookNode.availabilityStatus:
                bookNode.availabilityStatus = False
                bookNode.borrowedBy = patronID
                self.write_to_file(f"Book {bookID} Borrowed by Patron {patronID}")
            else:
                if len(bookNode.reservationHeap.heap) < 20:
                    # Include the current timestamp in the reservation
                    current_timestamp = time.time()
                    bookNode.reservationHeap.insert(patronID, patronPriority, current_timestamp)
                    self.write_to_file(f"Book {bookID} Reserved by Patron {patronID}")
                else:
                    self.write_to_file("Reservation list is full.")
        else:
            self.write_to_file(f"Book {bookID} not found.")

    def return_book(self, patronID, bookID):
        bookNode = self.bookTree.search(bookID)
        if bookNode != self.bookTree.nilNode and bookNode.borrowedBy == patronID:
            if not bookNode.reservationHeap.is_empty():
                next_patron = bookNode.reservationHeap.extract_min()
                bookNode.borrowedBy = next_patron.patronID
                self.write_to_file(f"Book {bookID} Returned by Patron {patronID}\nBook {bookID} Allotted to Patron {next_patron.patronID}")
            else:
                bookNode.availabilityStatus = True
                bookNode.borrowedBy = None
                self.write_to_file(f"Book {bookID} Returned by Patron {patronID}")
        else:
            self.write_to_file(f"Book {bookID} not currently borrowed by Patron {patronID}.")

    def delete_book(self, bookID):
        bookNode = self.bookTree.search(bookID)
        if bookNode != self.bookTree.nilNode:
            if not bookNode.reservationHeap.is_empty():
                reservations = [reservation.patronID for reservation in bookNode.reservationHeap.heap]
                if len(reservations) > 1:
                    self.write_to_file(f"Book {bookID} is no longer available. Reservations made by Patrons {', '.join(reservations)} have been cancelled!")
                else:
                    self.write_to_file(f"Book {bookID} is no longer available. Reservation made by Patron {reservations[0]} has been cancelled!")
            else:
                self.write_to_file(f"Book {bookID} is no longer available.")
            self.bookTree.delete_node(bookID)
        else:
            self.write_to_file(f"Book {bookID} not found in the library.")

    def find_closest_book(self, targetID):
        lower_book = self._find_closest_lower(self.bookTree.root, targetID, None)
        higher_book = self._find_closest_higher(self.bookTree.root, targetID, None)

        # Adjust logic to handle the case where the target book itself is found
        if lower_book and higher_book and lower_book.bookID == higher_book.bookID:
            # Only one book found (target book itself), print its details
            self._print_book_details(lower_book)
            return

        if lower_book and higher_book:
            # Calculate the distance to the targetID for both books
            lower_diff = targetID - lower_book.bookID
            higher_diff = higher_book.bookID - targetID

            # Print both books if they are equally close to the targetID
            if lower_diff == higher_diff:
                self._print_book_details(lower_book)
                self._print_book_details(higher_book)
                return

        # If only one book is found or one is closer, print it
        if lower_book and (not higher_book or lower_diff < higher_diff):
            self._print_book_details(lower_book)
        elif higher_book:
            self._print_book_details(higher_book)
        else:
            self.write_to_file(f"No closest book found for BookID {targetID}.")


    def _find_closest_lower(self, node, targetID, closest):
        if node == self.bookTree.nilNode:
            return closest
        if node.bookID <= targetID:
            closest = node
            return self._find_closest_lower(node.right, targetID, closest)
        else:
            return self._find_closest_lower(node.left, targetID, closest)

    def _find_closest_higher(self, node, targetID, closest):
        if node == self.bookTree.nilNode:
            return closest
        if node.bookID >= targetID:
            closest = node
            return self._find_closest_higher(node.left, targetID, closest)
        else:
            return self._find_closest_higher(node.right, targetID, closest)

    def _print_book_details(self, bookNode):
        availability = "Yes" if bookNode.availabilityStatus else "No"
        borrowedBy = bookNode.borrowedBy if bookNode.borrowedBy else "None"
        reservations = [reservation.patronID for reservation in bookNode.reservationHeap.heap]
        self.write_to_file(f"BookID = {bookNode.bookID}\nTitle = \"{bookNode.bookName}\"\nAuthor = \"{bookNode.authorName}\"\nAvailability = \"{availability}\"\nBorrowedBy = {borrowedBy}\nReservations = {reservations}")

    def color_flip_count(self):
        return self.bookTree.get_color_flip_count()





def main(input_filename):
    
    output_filename = input_filename.split('.')[0] + "_output_file.txt"
    library_system = LibrarySystem(output_filename)

    try:
        with open(input_filename, 'r') as infile:
            for line in infile:
                command = line.strip()

                # command = input("Enter command: ")
                # #print(f"Received command: {command}")
                try:
                    if command.startswith("InsertBook"):
                        # Remove 'InsertBook(' from the start and ')' from the end
                        argument_str = command[11:-1]

                        # Initialize variables
                        parts = []
                        current_part = ''
                        in_quotes = False

                        # Parse the command string
                        for char in argument_str:
                            if char == '"' and not in_quotes:  # Starting quote
                                in_quotes = True
                                current_part += char  # Include the quote in the current part
                            elif char == '"' and in_quotes:  # Ending quote
                                in_quotes = False
                                current_part += char  # Include the quote in the current part
                            elif char == ',' and not in_quotes:  # If not within quotes, this comma separates arguments
                                parts.append(current_part.strip())
                                current_part = ''
                            else:
                                current_part += char  # Build the current argument character by character

                        # Add the last part after the loop finishes
                        parts.append(current_part.strip())

                        # Unpack the parts list into individual variables
                        if len(parts) == 4:
                            bookID, title, author, availability = [part.strip().strip('"') for part in parts]
                            availabilityStatus = availability.lower()

                            # Call insert_book with the parsed arguments
                            library_system.insert_book(int(bookID), title, author, availabilityStatus, None)
                        else:
                            # Handle invalid command format
                            library_system.write_to_file(f"Invalid format for command: {command}")

                    elif command.startswith("PrintBooks("):
                        # Correctly extract the arguments from "PrintBooks" command
                        args_str = command[len("PrintBooks("):-1]
                        bookID1_str, bookID2_str = args_str.split(',')
                        bookID1 = int(bookID1_str.strip())
                        bookID2 = int(bookID2_str.strip())
                        library_system.print_books(bookID1, bookID2)

                    elif command.startswith("PrintBook("):
                        bookID = int(command[len("PrintBook("):-1].strip())
                        library_system.print_book(bookID)

                    

                    elif command.startswith("BorrowBook"):
                        patronID, bookID, patronPriority = command[len("BorrowBook("):-1].split(",")
                        library_system.borrow_book(patronID.strip(), int(bookID.strip()), int(patronPriority.strip()))

                    elif command.startswith("ReturnBook"):
                        patronID, bookID = command[len("ReturnBook("):-1].split(",")
                        library_system.return_book(patronID.strip(), int(bookID.strip()))

                    elif command.startswith("DeleteBook"):
                        bookID = int(command[len("DeleteBook("):-1].strip())
                        library_system.delete_book(bookID)

                    elif command.startswith("FindClosestBook"):
                        targetID = int(command[len("FindClosestBook("):-1].strip())
                        library_system.find_closest_book(targetID)

                    elif command.startswith("ColorFlipCount()"):
                        library_system.write_to_file(f"Colour Flip Count: {library_system.color_flip_count()}")

                    elif command == "Quit()":
                        library_system.write_to_file("Program Terminated!!")
                        break

                    else:
                        library_system.write_to_file("Invalid command")


                except Exception as e:
                    library_system.write_to_file(f"An error occurred while processing command '{command}': {e}\n")

    except Exception as e:
        library_system.write_to_file(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
    else:
        main(sys.argv[1])


