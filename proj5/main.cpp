#include "LinkedList.hpp"
#include <iostream>

int main() {

    LinkedList<int> list;
    list.push(1);
    list.push(2);
    list.push(3);
    LinkedListIterator<int> i = list.getIter();
    while (!i.isDone()) {
        std::cout << i.next() << std::endl;
    }
    list.push(4);
    list.push(5);

    std::cout << list.pop() << std::endl;
    std::cout << list.pop() << std::endl;
    std::cout << list.pop() << std::endl;

    return 0;
}
    