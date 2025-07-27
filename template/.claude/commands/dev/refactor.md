# /dev:refactor

Refactors code for improved quality, performance, and maintainability.

## Usage
`/dev:refactor <target> [focus]`

## Description
Systematically improves existing code without changing functionality, focusing on code quality, performance optimization, or architectural improvements.

## Refactoring Types

### 1. Code Quality
- Simplify complex methods
- Extract reusable components
- Improve naming
- Reduce duplication

### 2. Performance
- Optimize algorithms
- Improve database queries
- Add caching
- Reduce memory usage

### 3. Architecture
- Apply design patterns
- Improve modularity
- Enhance testability
- Reduce coupling

### 4. Maintainability
- Add type hints
- Improve documentation
- Standardize patterns
- Simplify logic

## Examples

### Refactor for Performance
```
/dev:refactor src/services/data_processor.py performance
```

### Refactor for Quality
```
/dev:refactor src/api/ quality
```

### Refactor Complex Method
```
/dev:refactor "OrderService.calculate_total method is too complex"
```

### Apply Design Pattern
```
/dev:refactor src/factories/ "implement factory pattern"
```

## Refactoring Process

### 1. Analysis
- Measure current metrics
- Identify code smells
- Plan improvements
- Assess impact

### 2. Implementation
- Make incremental changes
- Maintain functionality
- Update tests
- Preserve behavior

### 3. Validation
- Run all tests
- Verify performance
- Check functionality
- Review changes

## Common Refactoring Patterns

### Extract Method
**Before**:
```python
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Order has no items")
    if order.total < 0:
        raise ValueError("Invalid total")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError("Invalid quantity")
    
    # Calculate tax
    tax_rate = 0.08
    if order.shipping_address.state == "CA":
        tax_rate = 0.0975
    elif order.shipping_address.state == "NY":
        tax_rate = 0.085
    tax = order.subtotal * tax_rate
    
    # Process payment
    # ... more code
```

**After**:
```python
def process_order(order):
    validate_order(order)
    tax = calculate_tax(order)
    process_payment(order, tax)

def validate_order(order):
    if not order.items:
        raise ValueError("Order has no items")
    if order.total < 0:
        raise ValueError("Invalid total")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError("Invalid quantity")

def calculate_tax(order):
    tax_rates = {
        "CA": 0.0975,
        "NY": 0.085,
        "DEFAULT": 0.08
    }
    rate = tax_rates.get(order.shipping_address.state, tax_rates["DEFAULT"])
    return order.subtotal * rate
```

### Replace Conditional with Polymorphism
**Before**:
```python
class PaymentProcessor:
    def process(self, payment_type, amount):
        if payment_type == "credit_card":
            # Process credit card
            fee = amount * 0.029 + 0.30
            # ... processing logic
        elif payment_type == "paypal":
            # Process PayPal
            fee = amount * 0.034 + 0.49
            # ... processing logic
        elif payment_type == "bank_transfer":
            # Process bank transfer
            fee = 0 if amount > 1000 else 25
            # ... processing logic
```

**After**:
```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def calculate_fee(self, amount):
        pass
    
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def calculate_fee(self, amount):
        return amount * 0.029 + 0.30
    
    def process(self, amount):
        fee = self.calculate_fee(amount)
        # ... processing logic

class PayPalPayment(PaymentMethod):
    def calculate_fee(self, amount):
        return amount * 0.034 + 0.49
    
    def process(self, amount):
        fee = self.calculate_fee(amount)
        # ... processing logic

class BankTransferPayment(PaymentMethod):
    def calculate_fee(self, amount):
        return 0 if amount > 1000 else 25
    
    def process(self, amount):
        fee = self.calculate_fee(amount)
        # ... processing logic

# Usage
payment_methods = {
    "credit_card": CreditCardPayment(),
    "paypal": PayPalPayment(),
    "bank_transfer": BankTransferPayment()
}

def process_payment(payment_type, amount):
    method = payment_methods.get(payment_type)
    if not method:
        raise ValueError(f"Unknown payment type: {payment_type}")
    return method.process(amount)
```

### Optimize Database Queries
**Before**:
```python
def get_user_orders(user_id):
    user = User.query.get(user_id)
    orders = []
    for order in user.orders:
        order_data = {
            "id": order.id,
            "total": order.total,
            "items": []
        }
        for item in order.items:
            product = Product.query.get(item.product_id)
            order_data["items"].append({
                "product_name": product.name,
                "quantity": item.quantity,
                "price": item.price
            })
        orders.append(order_data)
    return orders
```

**After**:
```python
def get_user_orders(user_id):
    orders = (
        Order.query
        .filter_by(user_id=user_id)
        .options(
            joinedload(Order.items)
            .joinedload(OrderItem.product)
        )
        .all()
    )
    
    return [
        {
            "id": order.id,
            "total": order.total,
            "items": [
                {
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in order.items
            ]
        }
        for order in orders
    ]
```

## Refactoring Metrics

### Before/After Comparison
```markdown
# Refactoring Results

## Code Metrics
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Cyclomatic Complexity | 15 | 6 | -60% |
| Lines of Code | 250 | 180 | -28% |
| Test Coverage | 65% | 92% | +41% |
| Duplication | 18% | 3% | -83% |

## Performance Metrics
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Response Time (p95) | 450ms | 120ms | -73% |
| Memory Usage | 512MB | 320MB | -37% |
| Database Queries | 50 | 3 | -94% |
```

## Options

- `--focus`: Specific focus area (quality/performance/architecture)
- `--pattern`: Apply specific design pattern
- `--metric`: Target specific metric improvement
- `--safe`: Only safe refactorings (no behavior change)

## Safety Checklist

- [ ] All tests passing
- [ ] No functionality changed
- [ ] Performance maintained/improved
- [ ] Backwards compatibility preserved
- [ ] Documentation updated
- [ ] Code reviewed

## Best Practices

### 1. Incremental Changes
- Small, focused refactorings
- One type of change at a time
- Commit frequently
- Easy rollback

### 2. Test Coverage
- Ensure tests exist first
- Add tests if missing
- Run tests after each change
- Update tests as needed

### 3. Performance Monitoring
- Measure before and after
- Profile critical paths
- Monitor in production
- Set performance budgets

## Related Commands

- `/dev:review` - Review refactored code
- `/dev:test` - Ensure test coverage
- `/dev:debug` - Fix any issues
- `/git:commit` - Commit refactoring