

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

const modules = [
  "Workflow",
  "Item Management",
  "BOM Management",
  "Change Management",
  "Dataset Management",
  "Access Control",
  "Supplier Collaboration"
];

export default function TestCaseGeneratorApp() {
  const [input, setInput] = useState("");
  const [selectedModules, setSelectedModules] = useState([]);
  const [testCases, setTestCases] = useState([]);

  const toggleModule = (module) => {
    setSelectedModules((prev) =>
      prev.includes(module)
        ? prev.filter((m) => m !== module)
        : [...prev, module]
    );
  };


  const generateTestCases = () => {
    if (!input || selectedModules.length === 0) return;


    const text = input.toLowerCase();
    let generated = [];
    selectedModules.forEach((module) => {
      generated.push({
        id: `TC_${Date.now()}_${module}`,
        module,
        title: `${module} - Basic Validation`,
        preconditions: "User logged into Teamcenter",
        steps: [
          "Login to Teamcenter",
          `Navigate to ${module}`,
          "Perform operation",
          "Validate outcome"
        ],
        expected: "System behaves correctly",
        priority: "High"
      });

      if (module === "Workflow") {
        generated.push({
          id: `TC_${Date.now()}_WF`,
          module,
          title: "Workflow Initiation",
          preconditions: "Item exists",
          steps: [
            "Select object",
            "Start workflow",
            "Verify process created"
          ],
          expected: "Workflow started",
          priority: "High"
        });

        if (text.includes("approval")) {
          generated.push({
            id: `TC_${Date.now()}_APP`,
            module,
            title: "Approval Flow",
            preconditions: "Workflow initiated",
            steps: ["Approve task", "Verify next stage"],
            expected: "Moves forward",
            priority: "High"
          });
        }
        if (text.includes("rejection")) {
          generated.push({
            id: `TC_${Date.now()}_REJ`,
            module,
            title: "Rejection Flow",
            steps: ["Reject task", "Verify rollback"],
            expected: "Returns to initiator",
            priority: "Medium"
          });
        }
      }
    });
    if (text.includes("user") || text.includes("group")) {
      generated.push({
        id: `TC_${Date.now()}_USR`,
        module: "Common",
        title: "User Assignment",
        steps: [
          "Check assigned users",
          "Verify correct group"
        ],
        expected: "Correct assignment",
        priority: "High"
      });
    }


    generated.push({
      id: `TC_${Date.now()}_E2E`,
      module: "Common",
      title: "End-to-End Test",
      steps: [
        "Execute full flow",
        "Validate final output"
      ],
      expected: "Flow completed",
      priority: "High"
    });

    setTestCases(generated);
  };

  const exportCSV = () => {
    const headers = ["ID", "Module", "Title", "Preconditions", "Steps", "Expected", "Priority"];
    const rows = testCases.map(tc => [
      tc.id,
      tc.module,
      tc.title,
      tc.preconditions || "",
      tc.steps.join(" | "),
      tc.expected,
      tc.priority
    ]);


    const csvContent = [headers, ...rows]
      .map(e => e.join(","))
      .join("
");


    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "test_cases.csv";
    a.click();
  };


  return (
    <div className="p-6 grid gap-6">
      <Card>
        <CardContent>
          <h1>Teamcenter Test Case Generator</h1>
          <p>Select Modules</p>
          <div className="flex flex-wrap gap-2 mb-4">
            {modules.map((mod) => (
              <button
                key={mod}
                className={`px-3 py-1 border rounded ${selectedModules.includes(mod) ? "bg-blue-500 text-white" : ""}`}
                onClick={() => toggleModule(mod)}
              >
                {mod}
              </button>
            ))}
          </div>
          <Textarea
            placeholder="Enter requirement"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />

          <Button className="mt-4" onClick={generateTestCases}>
            Generate
          </Button>
        </CardContent>
      </Card>

      {testCases.length > 0 && (
        <Card>
          <CardContent>
            <h2>Generated Test Cases</h2>

            <Button className="mb-3" onClick={exportCSV}>
              Export to CSV
            </Button>


            <p>Total Test Cases: {testCases.length}</p>
            <p>Modules Covered: {selectedModules.join(", ")}</p>


            {testCases.map((tc) => (
              <div key={tc.id} className="border p-3 mb-2">
                <h3>{tc.title}</h3>
                <p><b>Module:</b> {tc.module}</p>
                <p><b>Preconditions:</b> {tc.preconditions}</p>
                <ul>
                  {tc.steps.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
                <p><b>Expected:</b> {tc.expected}</p>
                <p><b>Priority:</b> {tc.priority}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
