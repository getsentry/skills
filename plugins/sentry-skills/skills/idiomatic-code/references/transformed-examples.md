# Transformed Examples

These are directly reusable examples of the style this skill should produce.

## Happy Path: Plain, oRPC-Like Router Surface

### Before

```ts
type MemberAction = "list" | "invite";

type ExecuteMemberRequest = {
  action: MemberAction;
  organizationId: string;
  payload?: unknown;
};

export function createMemberService(context: AppContext) {
  return {
    async execute(request: ExecuteMemberRequest) {
      if (request.action === "list") {
        return listMembers(context, request.organizationId);
      }

      if (request.action === "invite") {
        return inviteMember(context, request.organizationId, request.payload as InviteMemberInput);
      }

      throw new Error(`Unsupported member action: ${request.action}`);
    },
  };
}
```

### After

```ts
export const memberRouter = {
  list: protectedProcedure
    .input(ListMembersInput)
    .handler(({ context, input }) => {
      return listMembers(context, input.organizationId);
    }),

  invite: protectedProcedure
    .input(InviteMemberInput)
    .handler(({ context, input }) => {
      return inviteMember(context, input.organizationId, input.email);
    }),
};
```

Why this is better:

- The public surface names the available operations directly.
- Consumers no longer pass a behavior-switching `action`.
- The router reads like a small object of obvious capabilities.

## Robust Variant: Explicit Failure Contract

### Before

```ts
export async function fetchProject(api: ApiClient, projectId: string) {
  const response = await api.get(`/projects/${projectId}`);

  if (!response.ok) {
    throw new Error("Unable to fetch project");
  }

  return response.json();
}
```

### After

```ts
export type GetProjectResult =
  | { ok: true; project: Project }
  | { ok: false; error: "not_found" | "forbidden" | "network_error" };

/**
 * Return one visible project.
 *
 * Expected failures are returned as tagged values.
 * Unexpected failures may still throw.
 */
export async function getProject(
  api: ApiClient,
  input: { projectId: string },
): Promise<GetProjectResult> {
  const response = await api.get(`/projects/${input.projectId}`);

  if (response.status === 404) {
    return { ok: false, error: "not_found" };
  }

  if (response.status === 403) {
    return { ok: false, error: "forbidden" };
  }

  if (!response.ok) {
    return { ok: false, error: "network_error" };
  }

  return {
    ok: true,
    project: await response.json(),
  };
}
```

Why this is better:

- The function name describes the job directly.
- The input shape is explicit and stable.
- Expected failures are visible to the caller and documented in one short comment.

## Anti-Pattern And Correction: Split Generic Workflows By Meaning

### Before

```ts
type SaveThingInput = {
  entityId?: string;
  payload: Record<string, unknown>;
  shouldValidate?: boolean;
  sendNotifications?: boolean;
  mode?: "create" | "update";
};

export async function saveThing(input: SaveThingInput): Promise<unknown> {
  if (input.shouldValidate) {
    await validate(input.payload);
  }

  if (input.mode === "update") {
    return updateEntity(input.entityId!, input.payload, input.sendNotifications === true);
  }

  return createEntity(input.payload, input.sendNotifications === true);
}
```

### After

```ts
export type CreateEntityInput = {
  payload: Record<string, unknown>;
  notify: boolean;
};

export async function createEntityRecord(input: CreateEntityInput): Promise<Entity> {
  await validate(input.payload);
  return createEntity(input.payload, input.notify);
}

export type UpdateEntityInput = {
  entityId: string;
  payload: Record<string, unknown>;
  notify: boolean;
};

export async function updateEntityRecord(input: UpdateEntityInput): Promise<Entity> {
  await validate(input.payload);
  return updateEntity(input.entityId, input.payload, input.notify);
}
```

Why this is better:

- Create and update are different jobs, so they get different names.
- Validation is no longer hidden behind a flag.
- Callers do not need to infer required fields from `mode`.

## Python Example: Contract-Focused Docstring

### Before

```python
def fetch_user(client, user_id, include_teams=False):
    """Fetch a user."""
    response = client.get(f"/users/{user_id}", include_teams=include_teams)
    response.raise_for_status()
    return response.json()
```

### After

```python
def fetch_user(client: APIClient, user_id: str, *, include_teams: bool = False) -> User:
    """Return one user by ID.

    Raises:
        UserNotFound: If the user does not exist.
        APIError: If the request fails for any other reason.
    """
    response = client.get(f"/users/{user_id}", include_teams=include_teams)
    response.raise_for_status()
    return response.json()
```

Why this is better:

- The signature makes optional behavior explicit.
- The first line says exactly what the caller gets.
- The docstring documents expected failures instead of repeating the body.

## Framework Boundary Example: Keep Naming, Remove Directive Magic

### Before

```tsx
'use client';

import { updateProjectAction } from './actions';

export function ProjectSettingsForm({ projectId }: { projectId: string }) {
  async function save(formData: FormData) {
    await updateProjectAction(formData);
  }

  return (
    <form action={save}>
      <input type="hidden" name="projectId" value={projectId} />
      <input name="name" />
      <button type="submit">Save</button>
    </form>
  );
}
```

```ts
'use server';

export async function updateProjectAction(formData: FormData) {
  const projectId = String(formData.get('projectId'));
  const name = String(formData.get('name'));
  return updateProjectInDatabase(projectId, name);
}
```

### After

```ts
export type UpdateProjectInput = {
  projectId: string;
  name: string;
};

export async function updateProject(input: UpdateProjectInput): Promise<Project> {
  return updateProjectInDatabase(input.projectId, input.name);
}
```

```ts
'use server';

import { updateProject } from './project-service';

export async function submitProjectSettings(formData: FormData): Promise<void> {
  await updateProject({
    projectId: String(formData.get('projectId')),
    name: String(formData.get('name')),
  });
}
```

```tsx
import { submitProjectSettings } from './actions';

export function ProjectSettingsForm({ projectId }: { projectId: string }) {
  return (
    <form action={submitProjectSettings}>
      <input type="hidden" name="projectId" value={projectId} />
      <input name="name" />
      <button type="submit">Save</button>
    </form>
  );
}
```

Why this is better:

- The domain operation is a plain function with an explicit input type.
- The framework-specific action wrapper stays at the edge instead of defining the core interface.
- The file naming and structure can stay conventional without making the business behavior depend on extra client-side directive magic.
