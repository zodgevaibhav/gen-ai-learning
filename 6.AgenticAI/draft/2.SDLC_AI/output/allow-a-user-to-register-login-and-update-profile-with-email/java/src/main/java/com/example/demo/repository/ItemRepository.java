package com.example.demo.repository;

import com.example.demo.dto.ItemDTO;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class ItemRepository {
    private final Map<Long, ItemDTO> itemStore = new HashMap<>();
    private long currentId = 1;

    public List<ItemDTO> findAll() {
        return new ArrayList<>(itemStore.values());
    }

    public ItemDTO findById(Long id) {
        return itemStore.get(id);
    }

    public ItemDTO save(ItemDTO itemDTO) {
        itemDTO.setId(currentId++);
        itemStore.put(itemDTO.getId(), itemDTO);
        return itemDTO;
    }

    public ItemDTO update(Long id, ItemDTO itemDTO) {
        itemDTO.setId(id);
        itemStore.put(id, itemDTO);
        return itemDTO;
    }

    public void delete(Long id) {
        itemStore.remove(id);
    }
}
```

### 7. Build Configuration (Gradle)
```groovy
