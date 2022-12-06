#include "LinkedList.hpp"
#include "SmartPointer.hpp"

/**
 * This is an example where the SmartPointer class fails because
 * each SmartPointer has a reference to the other one. Thus, when
 * either one goes out of scope, it will see that something else
 * still has a reference to it and not delete the SmartPointer, so
 * the contained reference will also remain, and neither of the
 * SmartPointers will be able to release the memory they contain.
*/

int main()
{
    SmartPointer<Node<int>> node1 = new Node<int>(1);
    SmartPointer<Node<int>> node2 = new Node<int>(2);

    node1->setNext(node2);
    node2->setNext(node1);

    return 0;
}
