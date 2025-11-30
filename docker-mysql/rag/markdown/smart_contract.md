## 定义
- 自动化执行的链上代码逻辑
- 无需第三方即可保证执行

## Solidity 示例
```solidity
pragma solidity ^0.8.0;
contract HelloWorld {
    string public message = "Hello Blockchain";

    function setMessage(string memory newMsg) public {
        message = newMsg;
    }
}
```

## 安全问题
- 重入攻击（Reentrancy）
- Gas 消耗优化
- 存储成本高
- 常用防御：使用 `checks-effects-interactions` 模式、OpenZeppelin 库