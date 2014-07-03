Realtrack Indicators Demo API
---
[Demo](http://neeraj2608.pythonanywhere.com/)

This is a small Flask web app that I hacked up to demo the use of an API for Realtrack Indicators. It runs off the same SQLite database that is used by the Realtrack Android app.

### Features

- Demo API for fetching VRF indicator data
- Conversion of XLS provided by Peace Corps into CSV/SQLite formats.

## API Endpoints

### Get VRF indicators

`GET /indicators`

**Params:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `project`  | `string` | `Required. project or sector to look up. e.g. Education` |
| `country`  | `string` | `Required. country to look up. e.g. Thailand` |

**Response:**

Success:
<pre>
{
  "indicatorlist": [
    {
      "goal": "Goal 1: Prevention & Sexual Health",
      "indicator": "Number of general population (NOT including MARPs/Key populations and PLHIV) reached with individual and/or small group level HIV prevention interventions that are based on evidence and/or meet the minimum standards required ",
      "objective": "Objective 1.1 HIV Sexual Health & HIV Prevention",
      "post": "Lesotho ", "project": "Youth"
    }
   --- snip ---
  ],
  "success": true
}
</pre>

Failure:
<pre>
{
  "error": "Invalid country and project combination",
  "success": false
}
</pre>

<pre>
{
  "error": "Both 'project' and 'country' request params are required.",
  "success": false
}
</pre>




Example API call:

[http://neeraj2608.pythonanywhere.com/indicators?project=Education&country=Thailand](http://neeraj2608.pythonanywhere.com/indicators?project=Education&country=Thailand)
