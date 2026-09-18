// src/services/archApiClient.js

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Internal variable to retain the active project ID across sequential steps
let currentProjectId = null;

/**
 * Getter and setter for the active project ID
 */
export function setProjectId(id) {
  currentProjectId = id;
}

export function getProjectId() {
  return currentProjectId;
}

/**
 * 1. Upload architecture diagram file to Backend, run Gemini Vision, and persist to DB
 * Endpoint: POST /api/v1/projects/upload
 * 
 * @param {File} file - The image file selected by the user
 * @returns {Promise<Object>} The newly created project and vision analysis payload
 */
export async function uploadDiagram(file) {
  if (!file) {
    throw new Error('A valid image file (PNG/JPEG) is required to upload.');
  }

  const formData = new FormData();
  formData.append('file', file);

  // Note: Do NOT set 'Content-Type': 'multipart/form-data' header manually.
  // The browser automatically sets boundary markers when using FormData.
  const response = await fetch(`${API_BASE_URL}/projects/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const errorDetail = errorBody.detail || `Upload failed with HTTP status ${response.status}`;
    throw new Error(errorDetail);
  }

  const data = await response.json();
  
  // Store the newly created project ID for subsequent calls
  currentProjectId = data.project_id;
  return data;
}

/**
 * Alias for backward compatibility if other components call createProject
 */
export const createProject = uploadDiagram;

/**
 * 2. Trigger the AI Multi-Agent Debate
 * Endpoint: POST /api/v1/projects/{project_id}/debate
 * 
 * @param {string} [projectId] - Optional project ID; defaults to currentProjectId
 * @returns {Promise<Object>} Debate report containing agents' arguments and primary risk
 */
export async function triggerDebate(projectId) {
  const id = projectId || currentProjectId;
  if (!id) {
    throw new Error('No active project ID found. Please upload a diagram first.');
  }

  const response = await fetch(`${API_BASE_URL}/projects/${id}/debate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const errorDetail = errorBody.detail || `Debate execution failed with HTTP status ${response.status}`;
    throw new Error(errorDetail);
  }

  return await response.json();
}

/**
 * 3. Submit Student Defense for AI Evaluation
 * Endpoint: POST /api/v1/projects/{project_id}/evaluate
 * 
 * @param {string} defenseText - The student's architectural defense
 * @param {string} [projectId] - Optional project ID; defaults to currentProjectId
 * @returns {Promise<Object>} Evaluation results, feedback scores, and corrected Mermaid diagram
 */
export async function submitDefense(defenseText, projectId) {
  const id = projectId || currentProjectId;
  if (!id) {
    throw new Error('No active project ID found. Please upload a diagram first.');
  }

  const response = await fetch(`${API_BASE_URL}/projects/${id}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_defense: defenseText }),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const errorDetail = errorBody.detail || `Evaluation failed with HTTP status ${response.status}`;
    throw new Error(errorDetail);
  }

  return await response.json();
}

/**
 * 4. Retrieve saved evaluation and corrected architecture
 * Endpoint: GET /api/v1/projects/{project_id}/evaluation
 */
export async function getEvaluation(projectId) {
  const id = projectId || currentProjectId;
  if (!id) {
    throw new Error('No active project ID specified.');
  }

  const response = await fetch(`${API_BASE_URL}/projects/${id}/evaluation`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Failed to fetch evaluation for project ${id}`);
  }

  return await response.json();
}