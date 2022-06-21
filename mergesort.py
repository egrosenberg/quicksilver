# Simple Merge Sort
# input, treeview to sort, tuple of iids of treeview, integer of value index to sort by
def sortTree(tree, iids, val):
    if len(iids) <= 1:
        return iids
    
    # Create left and right lists
    left = iids[:len(iids)//2]
    right = iids[len(iids)//2:len(iids):]
    # Recursively sort sublists
    left = sortTree(tree, left, val)
    right = sortTree(tree, right, val)
    # Merge final list
    print("recur")
    return merge(tree, left, right, val)

# Helper merge function
def merge(tree, l, r, val):
    out = []
    left = l
    right = r
    
    while (len(left) > 0) and (len(right) > 0):
        if tree.item(left[0])["values"][val] <= tree.item(right[0])["values"][val]:
            out.append(left[0])
            left = left[1:]
        else:
            out.append(right[0])
            right = right[1:]
    
    while len(left) > 0:
        out.append(left[0])
        left = left[1:]
    while len(right) > 0:
        out.append(right[0])
        right = right[1:]
    
    return out