# Property Dependencies Guide

Deep dive into n8n property dependencies and displayOptions mechanism.

---

## What Are Property Dependencies?

**Definition**: Rules that control when fields are visible or required based on other field values.

**Mechanism**: `displayOptions` in node schema

**Purpose**:
- Show relevant fields only
- Hide irrelevant fields
- Simplify configuration UX
- Prevent invalid configurations

---

## displayOptions Structure

### Basic Format

```javascript
{
  "name": "fieldName",
  "type": "string",
  "displayOptions": {
    "show": {
      "otherField": ["value1", "value2"]
    }
  }
}
```

**Translation**: Show `fieldName` when `otherField` equals "value1" OR "value2"

### Show vs Hide

#### show (Most Common)

**Show field when condition matches**:
```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true]
    }
  }
}
```

**Meaning**: Show `body` when `sendBody = true`

#### hide (Less Common)

**Hide field when condition matches**:
```javascript
{
  "name": "advanced",
  "displayOptions": {
    "hide": {
      "simpleMode": [true]
    }
  }
}
```

**Meaning**: Hide `advanced` when `simpleMode = true`

### Multiple Conditions (AND Logic)

```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**Meaning**: Show `body` when:
- `sendBody = true` AND
- `method IN (POST, PUT, PATCH)`

**All conditions must match** (AND logic)

### Multiple Values (OR Logic)

```javascript
{
  "name": "someField",
  "displayOptions": {
    "show": {
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**Meaning**: Show `someField` when:
- `method = POST` OR
- `method = PUT` OR
- `method = PATCH`

**Any value matches** (OR logic)

---

## Common Dependency Patterns

### Pattern 1: Boolean Toggle

**Use case**: Optional feature flag

**Example**: HTTP Request sendBody
```javascript
// Field: sendBody (boolean)
{
  "name": "sendBody",
  "type": "boolean",
  "default": false
}

// Field: body (depends on sendBody)
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true]
    }
  }
}
```

**Flow**:
1. User sees sendBody checkbox
2. When checked → body field appears
3. When unchecked → body field hides

### Pattern 2: Resource/Operation Cascade

**Use case**: Different operations show different fields

**Example**: Slack message operations
```javascript
// Operation: post
{
  "name": "channel",
  "displayOptions": {
    "show": {
      "resource": ["message"],
      "operation": ["post"]
    }
  }
}

// Operation: update
{
  "name": "messageId",
  "displayOptions": {
    "show": {
      "resource": ["message"],
      "operation": ["update"]
    }
  }
}
```

**Flow**:
1. User selects resource="message"
2. User selects operation="post" → sees channel
3. User changes to operation="update" → channel hides, messageId shows

### Pattern 3: Type-Specific Configuration

**Use case**: Different types need different fields

**Example**: IF node conditions
```javascript
// String operations
{
  "name": "value2",
  "displayOptions": {
    "show": {
      "conditions.string.0.operation": ["equals", "notEquals", "contains"]
    }
  }
}

// Unary operations (isEmpty) don't show value2
{
  "displayOptions": {
    "hide": {
      "conditions.string.0.operation": ["isEmpty", "isNotEmpty"]
    }
  }
}
```

### Pattern 4: Method-Specific Fields

**Use case**: HTTP methods have different options

**Example**: HTTP Request
```javascript
// Query parameters (all methods can have)
{
  "name": "queryParameters",
  "displayOptions": {
    "show": {
      "sendQuery": [true]
    }
  }
}

// Body (only certain methods)
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH", "DELETE"]
    }
  }
}
```

---

## Finding Property Dependencies

### Without tools: the tables, then the editor

1. **Know the operation's required fields** — the patterns in this file and in [OPERATION_PATTERNS.md](OPERATION_PATTERNS.md) list them per node.
2. **Import and look** — after import, a node that misses a required field shows red or a warning. Open it: n8n points at the field. A field you set that stays invisible is hidden by a parent field (e.g. `body` while `sendBody` is off).
3. **When unsure, copy from the editor** — let the lead build the node once in the n8n editor with the right operation, select it and copy it (Ctrl/Cmd+C). The pasted JSON shows the exact parameter names, nesting and `typeVersion`; base the import file on that. Say honestly when you don't know a field name rather than guessing.

### When to Dig Into Dependencies

**✅ Dig in when**:
- n8n flags a required field that you don't see in the node
- A field appears/disappears unexpectedly
- You need to understand what controls field visibility

**❌ Don't bother when**:
- Simple configuration
- Just starting configuration
- Field requirements are obvious

---

## Complex Dependency Examples

### Example 1: HTTP Request Complete Flow

**Scenario**: Configuring POST with JSON body

**Step 1**: Set method
```javascript
{
  "method": "POST"
  // → sendBody becomes visible
}
```

**Step 2**: Enable body
```javascript
{
  "method": "POST",
  "sendBody": true
  // → body field becomes visible AND required
}
```

**Step 3**: Configure body
```javascript
{
  "method": "POST",
  "sendBody": true,
  "body": {
    "contentType": "json"
    // → content field becomes visible AND required
  }
}
```

**Step 4**: Add content
```javascript
{
  "method": "POST",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "John",
      "email": "john@example.com"
    }
  }
}
// ✅ Complete: no warning on the node after import
```

**Dependency chain**:
```
method=POST
  → sendBody visible
    → sendBody=true
      → body visible + required
        → body.contentType=json
          → body.content visible + required
```

### Example 2: IF Node Operator Dependencies

**Scenario**: String comparison with different operators

**Binary operator** (equals):
```javascript
{
  "conditions": {
    "string": [
      {
        "operation": "equals"
        // → value1 required
        // → value2 required
        // → singleValue should NOT be set
      }
    ]
  }
}
```

**Unary operator** (isEmpty):
```javascript
{
  "conditions": {
    "string": [
      {
        "operation": "isEmpty"
        // → value1 required
        // → value2 should NOT be set
        // → singleValue should be true (auto-added)
      }
    ]
  }
}
```

**Dependency table**:

| Operator | value1 | value2 | singleValue |
|---|---|---|---|
| equals | Required | Required | false |
| notEquals | Required | Required | false |
| contains | Required | Required | false |
| isEmpty | Required | Hidden | true |
| isNotEmpty | Required | Hidden | true |

### Example 3: Slack Operation Matrix

**Scenario**: Different Slack operations show different fields

```javascript
// post message
{
  "resource": "message",
  "operation": "post"
  // Shows: channel (required), text (required), attachments, blocks
}

// update message
{
  "resource": "message",
  "operation": "update"
  // Shows: messageId (required), text (required), channel (optional)
}

// delete message
{
  "resource": "message",
  "operation": "delete"
  // Shows: messageId (required), channel (required)
  // Hides: text, attachments, blocks
}

// get message
{
  "resource": "message",
  "operation": "get"
  // Shows: messageId (required), channel (required)
  // Hides: text, attachments, blocks
}
```

**Field visibility matrix**:

| Field | post | update | delete | get |
|---|---|---|---|---|
| channel | Required | Optional | Required | Required |
| text | Required | Required | Hidden | Hidden |
| messageId | Hidden | Required | Required | Required |
| attachments | Optional | Optional | Hidden | Hidden |
| blocks | Optional | Optional | Hidden | Hidden |

---

## Nested Dependencies

### What Are They?

**Definition**: Dependencies within object properties

**Example**: HTTP Request body.contentType controls body.content structure

```javascript
{
  "body": {
    "contentType": "json",
    // → content expects JSON object
    "content": {
      "key": "value"
    }
  }
}

{
  "body": {
    "contentType": "form-data",
    // → content expects form fields array
    "content": [
      {
        "name": "field1",
        "value": "value1"
      }
    ]
  }
}
```

### How to Handle

**Strategy**: Configure parent first, then children

```javascript
// Step 1: Parent
{
  "body": {
    "contentType": "json"  // Set parent first
  }
}

// Step 2: Children (structure determined by parent)
{
  "body": {
    "contentType": "json",
    "content": {           // JSON object format
      "key": "value"
    }
  }
}
```

---

## Operator Structure and Missing Fields in the Import File

Nothing fixes the import file for you: what you write is what n8n loads.

### Operator structure (IF/Switch/Filter)

**Example**: singleValue property
```javascript
// You write (missing singleValue)
{
  "type": "boolean",
  "operation": "isEmpty"
  // Missing singleValue
}

// Write it complete: unary operators carry singleValue
{
  "type": "boolean",
  "operation": "isEmpty",
  "singleValue": true  // ✅ Set it yourself
}
```

If you are unsure of the exact operator shape, build one condition in the n8n editor, select the node, copy it (Ctrl/Cmd+C) and base the JSON on that.

### Missing required fields

**Missing required fields**:
```javascript
// You write (missing channel)
{
  "resource": "message",
  "operation": "post",
  "text": "Hello"
  // Missing required field: channel
}

// After import the node shows a red warning; add the field yourself
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",  // ← You must add
  "text": "Hello"
}
```

---

## Troubleshooting Dependencies

### Problem 1: "Field X is required but not visible"

**What you see**: after import the node is flagged ("body is required"), but you don't see a body field in the node.

**Solution**:
```javascript
// body only shows when sendBody=true (see the displayOptions above)
// Add sendBody
{
  "method": "POST",
  "sendBody": true,  // ← Now body appears!
  "body": {...}
}
```

### Problem 2: "Field disappears when I change operation"

**Scenario**:
```javascript
// Working configuration
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "Hello"
}

// Change operation
{
  "resource": "message",
  "operation": "update",  // Changed
  "channel": "#general",  // Still here
  "text": "Updated"       // Still here
  // Missing: messageId (required for update!)
}
```

**What n8n shows**: the node is flagged after import, "messageId is required"

**Why**: Different operation = different required fields

**Solution**:
```javascript
// Check requirements for the new operation (OPERATION_PATTERNS.md),
// or copy the node from the editor with that operation selected

// Configure for update operation
{
  "resource": "message",
  "operation": "update",
  "messageId": "1234567890",  // Required for update
  "text": "Updated",
  "channel": "#general"       // Optional for update
}
```

### Problem 3: "Import works but field doesn't save"

**Scenario**: Field hidden by dependencies; n8n drops it when the workflow is saved

**Example**:
```javascript
// Configure
{
  "method": "GET",
  "sendBody": true,  // ❌ GET doesn't support body
  "body": {...}      // This will be stripped
}

// After save
{
  "method": "GET"
  // body removed because method=GET hides it
}
```

**Solution**: Respect dependencies from the start

```javascript
// Correct approach - check property dependencies
// body only shows for POST/PUT/PATCH/DELETE
// Use correct method
{
  "method": "POST",
  "sendBody": true,
  "body": {...}
}
```

---

## Advanced Patterns

### Pattern 1: Conditional Required with Fallback

**Example**: Channel can be string OR expression

```javascript
// Option 1: String
{
  "channel": "#general"
}

// Option 2: Expression
{
  "channel": "={{$json.channelName}}"
}

// n8n accepts both
```

### Pattern 2: Mutually Exclusive Fields

**Example**: Use either ID or name, not both

```javascript
// Use messageId
{
  "messageId": "1234567890"
  // name not needed
}

// OR use messageName
{
  "messageName": "thread-name"
  // messageId not needed
}

// Dependencies ensure only one is required
```

### Pattern 3: Progressive Complexity

**Example**: Simple mode vs advanced mode

```javascript
// Simple mode
{
  "mode": "simple",
  "text": "{{$json.message}}"
  // Advanced fields hidden
}

// Advanced mode
{
  "mode": "advanced",
  "attachments": [...],
  "blocks": [...],
  "metadata": {...}
  // Simple field hidden, advanced fields shown
}
```

---

## Best Practices

### ✅ Do

1. **Check dependencies when stuck**
   ```javascript
   // Look up the parent field that shows it (tables in this file),
   // or copy the node from the n8n editor to see its real shape
   ```

2. **Configure parent properties first**
   ```javascript
   // First: method, resource, operation
   // Then: dependent fields
   ```

3. **Re-import and run after changing operation**
   ```javascript
   // Operation changed → requirements changed
   // Import, open the node, check for warnings, run it (Execute step)
   ```

4. **Read n8n's node warnings for dependency hints**
   ```
   Warning: "body required when sendBody=true"
   → Hint: Set sendBody=true to enable body
   ```

### ❌ Don't

1. **Don't ignore dependency errors**
   ```javascript
   // Error: "body not visible" → Check displayOptions
   ```

2. **Don't hardcode all possible fields**
   ```javascript
   // Bad: Adding fields that will be hidden
   ```

3. **Don't assume operations are identical**
   ```javascript
   // Each operation has unique requirements
   ```

---

## Summary

**Key Concepts**:
- `displayOptions` control field visibility
- `show` = field appears when conditions match
- `hide` = field disappears when conditions match
- Multiple conditions = AND logic
- Multiple values = OR logic

**Common Patterns**:
1. Boolean toggle (sendBody → body)
2. Resource/operation cascade (different operations → different fields)
3. Type-specific config (string vs boolean conditions)
4. Method-specific fields (GET vs POST)

**Troubleshooting**:
- Field required but not visible → Check dependencies
- Field disappears after change → Operation changed requirements
- Field doesn't save → Hidden by dependencies

**Where to look**:
- The patterns in this file and [OPERATION_PATTERNS.md](OPERATION_PATTERNS.md) - operation requirements
- The node after import - red/warning marks point at the missing field
- A node copied from the n8n editor (Ctrl/Cmd+C) - exact parameter names, nesting and typeVersion
- The INPUT and OUTPUT panels after a run - what actually arrives and leaves

**Related Files**:
- **[SKILL.md](SKILL.md)** - Main configuration guide
- **[OPERATION_PATTERNS.md](OPERATION_PATTERNS.md)** - Common patterns by node type

---

## Quick Reference: displayOptions and Common Dependency Patterns

A condensed introduction to the displayOptions mechanism and the three most common dependency patterns, plus how to find them.

### displayOptions Mechanism

**Fields have visibility rules**:

```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**Translation**: "body" field shows when:
- sendBody = true AND
- method = POST, PUT, or PATCH

### Common Dependency Patterns

#### Pattern 1: Boolean Toggle

**Example**: HTTP Request sendBody
```javascript
// sendBody controls body visibility
{
  "sendBody": true   // → body field appears
}
```

#### Pattern 2: Operation Switch

**Example**: Slack resource/operation
```javascript
// Different operations → different fields
{
  "resource": "message",
  "operation": "post"
  // → Shows: channel, text, attachments, etc.
}

{
  "resource": "message",
  "operation": "update"
  // → Shows: messageId, text (different fields!)
}
```

#### Pattern 3: Type Selection

**Example**: IF node conditions
```javascript
{
  "type": "string",
  "operation": "contains"
  // → Shows: value1, value2
}

{
  "type": "boolean",
  "operation": "equals"
  // → Shows: value1, value2, different operators
}
```

### Finding Property Dependencies

- Know the operation's required fields (the patterns above and [OPERATION_PATTERNS.md](OPERATION_PATTERNS.md)).
- After import, open a flagged node: n8n points at the field it misses.
- When unsure about names or nesting, let the lead build the node once in the n8n editor, select it and copy it (Ctrl/Cmd+C); the pasted JSON is the ground truth to base the import file on.

**Use this when**: n8n flags a node and you don't understand why a field is missing/required

---

## Handling Conditional Requirements

How to discover and satisfy fields that are required only under certain conditions.

### Example: HTTP Request Body

**Scenario**: body field required, but only sometimes

**Rule**:
```
body is required when:
  - sendBody = true AND
  - method IN (POST, PUT, PATCH, DELETE)
```

**How to discover**:
```javascript
// Option 1: Import and read the node warning
// "body required when sendBody=true"

// Option 2: Copy the node from the n8n editor
// Build it once with sendBody on, select, Ctrl/Cmd+C: shows body's real shape

// Option 3: Try minimal config and iterate
// Start without body, import, and see whether n8n flags it
```

### Example: IF Node singleValue

**Scenario**: singleValue property appears for unary operators

**Rule**:
```
singleValue should be true when:
  - operation IN (isEmpty, isNotEmpty, true, false)
```

**In the import file**: set `singleValue: true` on the operator yourself; nothing adds it for you.

**When unsure**: build the condition once in the n8n editor and copy the node (Ctrl/Cmd+C); the pasted JSON shows the operator shape.
