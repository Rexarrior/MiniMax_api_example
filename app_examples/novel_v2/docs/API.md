# API Documentation

## Stories

### List Stories
```
GET /api/stories
```

Returns a list of available stories.

### Get Story Info
```
GET /api/stories/{story_id}
```

Returns metadata for a specific story.

## Sessions

### Start Game
```
POST /api/sessions
{
  "story_id": "string"
}
```

Creates a new game session and returns the initial scene.

### Get Current Scene
```
GET /api/sessions/{session_id}
```

Returns the current scene state for a session.

### Make Choice
```
POST /api/sessions/{session_id}/choices
{
  "choice_index": 0
}
```

Submits a choice and returns the next scene.

### End Session
```
DELETE /api/sessions/{session_id}
```

Ends a game session.

## Health

### Health Check
```
GET /health
```

Returns service health status.
