#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <errno.h>

/**
 * Assignment 2: AVL Tree Implementation in C
 * For CSC 562-01, Spring 2018, Dr. Somya D. Mohanty
 * University of North Carolina at Greensboro
 *
 * @author James Knox Polk <jkpolk@uncg.edu>
 * @date 2/13/2019
 *
 * Usage: Implements an AVL Tree, first with hard-coded integer values to test functionality,
 * and then prompts for user input of 10 new integers to build a new tree.  The program will
 * print out both a pre-order traversal of the integers, as well as a indented structure model.
 *
 */


/**
 * Define the Node
 */
typedef struct node {
    int data;
    struct node *left;
    struct node *right;
    struct node *parent;
    int height;
} node;

/**
 * Initialize the node
 *
 * @param data
 * @param parent
 * @return node
 */
node *initNode(int data, node *parent) {
    node *n = malloc(sizeof(node));
    n->data = data;
    n->parent = parent;
    n->height = 1;
    n->left = NULL;
    n->right = NULL;

    return n;
}

/**
 * Find max value
 * @param a
 * @param b
 * @return
 */
int max(int a, int b) { return a > b ? a : b; }

/**
 * Find node insertion point
 *
 * @param root
 * @param data
 * @return root
 */
node *find(node *root, int data) {
    if (root == NULL) return NULL;
    if (data < root->data)
        return find(root->left, data);
    else if (data > root->data)
        return find(root->right, data);
    else
        return root;
}

/**
 * Get the height of the node
 *
 * @param root
 * @return height
 */
int getHeight(node *root) {
    return root ? root->height : 0;
}

/**
 * Adjust height of node for balancing
 *
 * @param root
 */
void adjustHeight(node *root) {
    root->height = 1 + max(getHeight(root->left), getHeight(root->right));
}

/**
 * Right rotation for balancing
 *
 * @param root
 * @return node
 */
node *rotateRight(node *root) {
    // Fix the pointers to the node
    node *new_root = root->left;
    if (root->parent) {
        if (root->parent->left == root) root->parent->left = new_root;
        else root->parent->right = new_root;
    }
    new_root->parent = root->parent;
    root->parent = new_root;
    root->left = new_root->right;
    if (root->left) root->left->parent = root;
    new_root->right = root;

    // Bottom-up adjustment of heights
    adjustHeight(root);
    adjustHeight(new_root);
    return new_root;
}

/**
 * Left rotation for balancing
 *
 * @param root
 * @return node
 */
node *rotateLeft(node *root) {
    // Fix the pointers to the node
    node *new_root = root->right;
    if (root->parent) {
        if (root->parent->right == root) root->parent->right = new_root;
        else root->parent->left = new_root;
    }
    new_root->parent = root->parent;
    root->parent = new_root;
    root->right = new_root->left;
    if (root->right) root->right->parent = root;
    new_root->left = root;

    // Bottom-up adjustment of heights
    adjustHeight(root);
    adjustHeight(new_root);
    return new_root;
}

/**
 * Perform Tree Balancing
 *
 * @param root
 * @return
 */
node *balanceTree(node *root) {
    if (getHeight(root->left) - getHeight(root->right) > 1) {
        if (getHeight(root->left->left) > getHeight(root->left->right)) {
            root = rotateRight(root);
        } else {
            rotateLeft(root->left);
            root = rotateRight(root);
        }
    } else if (getHeight(root->right) - getHeight(root->left) > 1) {
        if (getHeight(root->right->right) > getHeight(root->right->left)) {
            root = rotateLeft(root);
        } else {
            rotateRight(root->right);
            root = rotateLeft(root);
        }
    }
    return root;
}

/**
 * Insert a new node
 *
 * @param root
 * @param data
 * @return
 */
node *insertNode(node *root, int data) {
    node *current = root;
    while (current->data != data) {
        if (data < current->data) {
            if (current->left) current = current->left;
            else {
                current->left = initNode(data, current);
                current = current->left;
            }
        } else if (data > current->data) {
            if (current->right) current = current->right;
            else {
                current->right = initNode(data, current);
                current = current->right;
            }
        } else return root;
    }

    do {
        current = current->parent;
        adjustHeight(current);
        current = balanceTree(current);
    } while (current->parent);

    return current;
}

/**
 * Prints an indented representation of the tree of the form:
 *
 * Parent
 *      Left Child
 *      Right Child
 *
 * @param node
 * @param indent
 */
void printIndentedTree(node *node, int indent) {
    int pk;
    for (pk = 0; pk < indent; pk++) printf(" ");
    if (!node) printf("No child\n");
    else {
        printf("Node Value: %d; Height: %d\n", node->data, node->height);
        printIndentedTree(node->left, indent + 4);
        printIndentedTree(node->right, indent + 4);
    }
}

/**
 * Prints a space-separated pre-order traversal of the tree
 *
 * @param node
 */
void printPreorder(struct node *node) {
    if (node == NULL)
        return;

    printf("%d ", node->data);
    printPreorder(node->left);
    printPreorder(node->right);
}

/**
 * Print out the tree information
 * @param node
 */
void printTree(node *node) {
    printf("\nPreorder traversal of binary tree is: \n");
    printPreorder(node);
    printf("\n\nIndented tree diagram: \n");
    printIndentedTree(node, 0);
}

/**
 * Strtol to int conversion
 *
 * Code written by user chux at <https://stackoverflow.com/questions/6181432/why-is-there-no-strtoi-in-stdlib-h>
 * @param s
 * @param endptr
 * @param base
 * @return
 */
int strtoi(const char *s, char **endptr, int base) {
#if INT_MAX == LONG_MAX && INT_MIN == LONG_MIN
    return (int) strtol(s, endptr, base);
#else
    return (int) strto_subrange(s, endptr, base, INT_MIN, INT_MAX);
#endif
}

/**
 * Converts strtol to a defined subrange
 *
 * Code written by user chux at <https://stackoverflow.com/questions/6181432/why-is-there-no-strtoi-in-stdlib-h>
 * @param s
 * @param endptr
 * @param base
 * @param min
 * @param max
 * @return
 */
static long strto_subrange(const char *s, char **endptr, int base,
                           long min, long max) {
    long y = strtol(s, endptr, base);
    if (y > max) {
        errno = ERANGE;
        return max;
    }
    if (y < min) {
        errno = ERANGE;
        return min;
    }
    return y;
}

/**
 * Input validation
 * @param s
 * @return
 */
int isNumeric (const char * s)
{
    if (s == NULL || *s == '\0' || isspace(*s))
        return 0;
    char * p;
    strtoi (s, &p, 10);
    return *p == '\0';
}

int main(int argc, char *argv[]) {
    int n [10];
    int i = 0;
    int num;
    char term[20];
    char *end;

    while (i < 10) {
        printf("Please enter an integer ( %d of 10 entered): ", i);
        scanf("%s", term);

        if(isNumeric(term) == 0) {
            printf("Failure: please input a valid integer followed by enter key\n");
            continue;
        }
        num = strtoi(term, &end, 10);
        n[i] = num;
        i++;
    }

    printf("Building AVL Tree with the following user inputs: ");
    for (int j=0; j<10; j++) {
        printf("%d ", n[j]);
    }
    printf("\n\n");
    node *root = initNode(n[0], NULL);
    root = insertNode(root, n[1]);
    root = insertNode(root, n[2]);
    root = insertNode(root, n[3]);
    root = insertNode(root, n[4]);
    root = insertNode(root, n[5]);
    root = insertNode(root, n[6]);
    root = insertNode(root, n[7]);
    root = insertNode(root, n[8]);
    root = insertNode(root, n[9]);

    printTree(root);

    return 0;
}