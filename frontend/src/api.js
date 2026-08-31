const API_BASE_URL="http://127.0.0.1:8000";

async function request(endpoint,options={}){
const response=await fetch(`${API_BASE_URL}${endpoint}`,options);
if(!response.ok){
const text=await response.text();
throw new Error(`Backend returned ${response.status}: ${text}`);
}
return response.json();
}

export function checkBackend(){
return request("/health");
}

export function analyzeMovement(exercise,sequence){
return request("/analyze",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({exercise,sequence})
});
}