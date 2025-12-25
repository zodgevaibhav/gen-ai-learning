package com.example.demo.service;

import com.example.demo.dto.ItemDTO;
import com.example.demo.repository.ItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ItemServiceImpl implements ItemService {

    @Autowired
    private ItemRepository itemRepository;

    @Override
    public List<ItemDTO> getAllItems() {
        return itemRepository.findAll();
    }

    @Override
    public ItemDTO getItemById(Long id) {
        return itemRepository.findById(id);
    }

    @Override
    public ItemDTO createItem(ItemDTO itemDTO) {
        return itemRepository.save(itemDTO);
    }

    @Override
    public ItemDTO updateItem(Long id, ItemDTO itemDTO) {
        return itemRepository.update(id, itemDTO);
    }

    @Override
    public void deleteItem(Long id) {
        itemRepository.delete(id);
    }
}
```

### 6. In-Memory Repository
```java
