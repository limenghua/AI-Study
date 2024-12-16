  #include <vector>
  #include <iostream>
  struct ListNode {
      int val;
      ListNode *next;
      ListNode() : val(0), next(nullptr) {}
      ListNode(int x) : val(x), next(nullptr) {}
      ListNode(int x, ListNode *next) : val(x), next(next) {}


      static ListNode* createList(const std::vector<int>& nums) {
        if(nums.empty()) return nullptr;
        ListNode* head = new ListNode(nums[0]);
        ListNode* curr = head;
        for(int i = 1; i < nums.size(); i++) {
          curr->next = new ListNode(nums[i]);
          curr = curr->next;
        }
        return head;
      }

      static void printList(ListNode* head) {
        while(head) {
          std::cout << head->val << " ";
          head = head->next;
        }
        std::cout << std::endl;
      }


  };
