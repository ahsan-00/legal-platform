import http from 'k6/http';
import { check, sleep } from 'k6';

// SLA targets: P95 < 1.5s, error rate < 2%
export const options = {
  stages: [
    { duration: '10s', target: 50 },   // ramp up to 50 users
    { duration: '30s', target: 100 },  // hold at 100 users
    { duration: '10s', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1500'],  // P95 must be under 1.5s
    http_req_failed: ['rate<0.02'],     // error rate must be under 2%
  },
};

const BASE_URL = 'http://localhost:8000';

const queries = [
  'Data Protection',
  'Contract Law',
  'Employment Standards',
  'Cybersecurity',
  'Consumer Protection',
];

export default function () {
  const query = queries[Math.floor(Math.random() * queries.length)];

  const response = http.post(
    `${BASE_URL}/generate`,
    JSON.stringify({ query: query }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(response, {
    'status is 200': (r) => r.status === 200,
    'success is true': (r) => JSON.parse(r.body).success === true,
    'response time < 1500ms': (r) => r.timings.duration < 1500,
  });

  sleep(1);
}