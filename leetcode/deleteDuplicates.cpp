#include <iostream>
#include <vector>
#include <unordered_set>

#include "ListNode.hpp"

using namespace std;

class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        if (head == nullptr) {
            return nullptr;
        }
        unordered_set<int> seen;
        seen.insert(head->val);
        ListNode* prev = head;
        ListNode* curr = head->next;
        while (curr!= nullptr) {
            if(curr->val == prev->val) {
                prev->next = curr->next;
            } else {
                prev = curr;
            }
            curr = prev->next;
        }
        return head;
    }
};

int main() {
    Solution s;
    vector<int> nums = {1,1,2,3,3};
    ListNode* head = createList(nums);
    ListNode* res = s.deleteDuplicates(head);
    printList(res);
    return 0;
}