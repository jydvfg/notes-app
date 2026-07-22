# Tool Calling Protocol
When calling tools, you MUST format your response as strict JSON wrapped inside a markdown code block:

```json
{
  "name": "tool_name",
  "arguments": {
    "key": "value"
  }
}