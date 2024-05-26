# GatorLibrary System with Red-Black Tree and Min-Heap Implementation
 

# GatorLibrary Management System

## Overview

The GatorLibrary Management System is designed to provide a reliable and effective method for managing workflows related to tracking, borrowing, and reserving books. It employs a Red-Black Tree data structure to ensure optimized search, insert, and delete operations, which are critical for maintaining an extensive library catalog. Additionally, a priority-queue system based on Binary Min-heaps is integrated to handle customer reservations efficiently, respecting both timeliness and priority.

## Project Objectives

1. **Data Structure Implementation**: 
   - **Red-Black Tree**: Used for efficient management of book records, supporting insertion, deletion, and searching operations.
   - **Binary Min-Heap**: Incorporated within each book node to manage reservations effectively, allowing quick retrieval of the highest priority reservation.

2. **Library Operations**:
   - **Adding Books**: Insert new book records into the system.
   - **Borrowing Books**: Handle automated reservations if the book is unavailable.
   - **Returning Books**: Allocate returned books to the next patron in the priority queue.
   - **Removing Books**: Inform patrons of cancellations and delete book records.
   - **Finding Books**: Display information about the closest book by ID.
   - **Printing Book Information**: Print details about individual books or a range of books.
   - **Tracking Structural Changes**: Report the frequency of structural changes within the Red-Black Tree, specifically color flips.

3. **Priority and Timestamp Accuracy**: 
   - Manage patron reservations with high accuracy, ensuring the priority system respects both the priority number and the timestamp for fair and consistent processing.

## Steps to Run

1. **Environment Setup**:
   - Ensure Python and Visual Studio Code are installed.

2. **Running the Project**:
   - Unzip `Ganti_Balasai_Srikanth.zip` and open the folder.
   - Open a terminal in the project directory.
   - Run one of the following commands:
     ```bash
     python gatorLibrary.py <Input_FileName>
     ```
     or
     ```bash
     python3 gatorLibrary.py <Input_FileName>
     ```
   - The output will be generated in `<Input_FileName>_output_file.txt`.

## Code Structure

The project consists of the following core classes:

1. **RedBlackTreeNode**: Represents a book and its related information.
2. **RedBlackTree**: Manages a collection of books using a Red-Black Tree data structure.
3. **HeapNode**: Represents a node in the heap, storing information about a patron's reservation.
4. **BinaryMinHeap**: Manages library patron reservations using a binary min-heap data structure.
5. **LibrarySystem**: Represents the library management system, utilizing the above classes to handle various operations.

### RedBlackTreeNode Class

- **Initialization**: Initializes the properties of a book.
- **Time Complexity**: O(1)
- **Space Complexity**: O(1)

### RedBlackTree Class

- **Initialization**: Sets up the tree with a nil node and root.
- **Rotations**: Performs left and right rotations to maintain tree balance.
- **Insert and Delete Operations**: Ensures efficient management of book records.
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

### HeapNode Class

- **Attributes**: Patron ID, priority number, and reservation time.
- **Comparison Methods**: Used for comparing priority and reservation times.
- **Time and Space Complexity**: O(1)

### BinaryMinHeap Class

- **Heap Operations**: Insert, extract, sift up, and sift down operations to maintain heap properties.
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

### LibrarySystem Class

- **Core Functions**: Insert, borrow, return, delete books, and find closest books.
- **Reservation Handling**: Manages book reservations using the Binary Min-Heap.
- **Color Flip Counting**: Tracks the number of color flips in the Red-Black Tree.

## Challenges

- **Color Flip Count**: Differences in color flip counts were observed, potentially due to variations in node replacement strategies during deletion operations.

## Conclusion

The GatorLibrary Management System effectively demonstrates the practical application of complex data structures in addressing real-world challenges in library management. The integration of Red-Black Trees and Binary Min-Heaps ensures optimal performance and equitable reservation handling. The project's focus on modular architecture and clean coding practices highlights its scalability and maintainability, laying a solid foundation for future enhancements in library management systems.
