package com.example.demo.service;

import com.example.demo.dto.ItemDTO;

import java.util.List;

public interface ItemService {
    List<ItemDTO> getAllItems();
    ItemDTO getItemById(Long id);
    ItemDTO createItem(ItemDTO itemDTO);
    ItemDTO updateItem(Long id, ItemDTO itemDTO);
    void deleteItem(Long id);
}
```

### 5. Service Implementation
```java
