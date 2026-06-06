// app.js

// --- Mock Database / System State ---
const state = {
  hosteller: {
    username: "johndoe",
    firstName: "John",
    lastName: "Doe",
    email: "johndoe@hostelsphere.edu",
    phoneNumber: "+91 98765 43210",
    yearOfStudy: "3",
    department: "Computer Science",
    hostelName: "Hostel A",
    roomNumber: "302",
    dob: "2004-06-06", // Make it today to trigger birthday alert
  },
  
  hostellersList: [
    { id: 101, firstName: "John", lastName: "Doe", email: "johndoe@hostelsphere.edu", phone: "+91 98765 43210", year: "3", dept: "Computer Science", hostel: "Hostel A", room: "302", dob: "2004-06-06" },
    { id: 102, firstName: "Alice", lastName: "Smith", email: "alice.smith@hostelsphere.edu", phone: "+91 87654 32109", year: "2", dept: "Electrical", hostel: "Hostel B", room: "108", dob: "2005-04-12" },
    { id: 103, firstName: "Bob", lastName: "Johnson", email: "bob.j@hostelsphere.edu", phone: "+91 76543 21098", year: "4", dept: "Mechanical", hostel: "Hostel A", room: "415", dob: "2003-11-22" },
    { id: 104, firstName: "Charlie", lastName: "Brown", email: "charlie.b@hostelsphere.edu", phone: "+91 65432 10987", year: "1", dept: "Computer Science", hostel: "Hostel C", room: "204", dob: "2006-06-06" }, // Birthday today!
    { id: 105, firstName: "Diana", lastName: "Prince", email: "diana.p@hostelsphere.edu", phone: "+91 54321 09876", year: "3", dept: "Computer Science", hostel: "Hostel B", room: "312", dob: "2004-08-30" },
    { id: 106, firstName: "Emma", lastName: "Watson", email: "emma.w@hostelsphere.edu", phone: "+91 43210 98765", year: "2", dept: "Electrical", hostel: "Hostel C", room: "115", dob: "2005-12-05" }
  ],
  
  attendance: {
    // Format: "YYYY-MM-DD": "P" / "A" / "L"
    "2026-06-01": "P",
    "2026-06-02": "P",
    "2026-06-03": "L",
    "2026-06-04": "P",
    "2026-06-05": "A",
  },
  
  outpassRequests: [
    {
      id: 1,
      userId: 101,
      firstName: "John",
      lastName: "Doe",
      requestDate: "2026-06-05 09:30",
      startDate: "2026-06-12",
      endDate: "2026-06-15",
      reason: "Going home for sister's wedding ceremony.",
      status: "Pending"
    },
    {
      id: 2,
      userId: 102,
      firstName: "Alice",
      lastName: "Smith",
      requestDate: "2026-06-04 14:20",
      startDate: "2026-06-08",
      endDate: "2026-06-10",
      reason: "Medical checkup at city hospital.",
      status: "Approved"
    },
    {
      id: 3,
      userId: 103,
      firstName: "Bob",
      lastName: "Johnson",
      requestDate: "2026-06-03 11:00",
      startDate: "2026-06-05",
      endDate: "2026-06-07",
      reason: "Inter-college athletic meet attendance.",
      status: "Rejected"
    }
  ],

  selectedDate: "2026-06-06"
};

// --- Calendar Initialization Helper ---
const calendarConfig = {
  year: 2026,
  month: 5 // June (0-indexed)
};

// --- DOM Nodes ---
document.addEventListener("DOMContentLoaded", () => {
  initApp();
  
  // Disclaimer Banner Close Handler
  const disclaimerBanner = document.getElementById("disclaimerBanner");
  const closeDisclaimerBtn = document.getElementById("closeDisclaimer");
  if (closeDisclaimerBtn && disclaimerBanner) {
    closeDisclaimerBtn.addEventListener("click", () => {
      disclaimerBanner.style.opacity = "0";
      setTimeout(() => {
        disclaimerBanner.style.display = "none";
      }, 500);
    });
  }
});

// Initialize dashboard elements
function initApp() {
  // Navigation for dashboards
  setupDashboardTabs();
  
  // Hosteller Dashboard Setups
  renderProfileInfo();
  buildCalendar();
  renderAttendanceTable();
  renderOutpassHistoryHosteller();
  setupOutpassForm();
  
  // Warden Dashboard Setups
  renderWardenStats();
  renderOutpassApprovalQueue();
  renderStudentRosterTable();
  setupStudentFilter();
  renderBirthdayAlerts();
}

// Switching Roles/Panels in Simulator
function setupDashboardTabs() {
  const hostellerTabBtn = document.getElementById("tabHosteller");
  const wardenTabBtn = document.getElementById("tabWarden");
  const hostellerScreen = document.getElementById("screenHosteller");
  const wardenScreen = document.getElementById("screenWarden");
  const windowTitle = document.getElementById("simulatorTitle");

  hostellerTabBtn.addEventListener("click", () => {
    hostellerTabBtn.className = "sidebar-btn active";
    wardenTabBtn.className = "sidebar-btn";
    hostellerScreen.classList.add("active");
    wardenScreen.classList.remove("active");
    windowTitle.innerText = "Hosteller Dashboard - " + state.hosteller.firstName + " " + state.hosteller.lastName;
    
    // Refresh tables since data might have changed
    renderOutpassHistoryHosteller();
    buildCalendar();
  });

  wardenTabBtn.addEventListener("click", () => {
    wardenTabBtn.className = "sidebar-btn active-warden";
    hostellerTabBtn.className = "sidebar-btn";
    wardenScreen.classList.add("active");
    hostellerScreen.classList.remove("active");
    windowTitle.innerText = "Warden Portal - Dashboard Overview";
    
    // Refresh stats & tables
    renderWardenStats();
    renderOutpassApprovalQueue();
    renderStudentRosterTable();
    renderBirthdayAlerts();
  });
}

// ==========================================
// HOSTELLER DASHBOARD FUNCTIONS
// ==========================================

function renderProfileInfo() {
  const fields = [
    { id: "profFirstName", val: state.hosteller.firstName },
    { id: "profLastName", val: state.hosteller.lastName },
    { id: "profEmail", val: state.hosteller.email },
    { id: "profPhone", val: state.hosteller.phoneNumber },
    { id: "profYear", val: state.hosteller.yearOfStudy + "rd Year" },
    { id: "profDept", val: state.hosteller.department },
    { id: "profHostel", val: state.hosteller.hostelName },
    { id: "profRoom", val: state.hosteller.roomNumber }
  ];
  
  fields.forEach(f => {
    const el = document.getElementById(f.id);
    if (el) el.innerText = f.val;
  });
}

// Generate Calendar GUI for June 2026
function buildCalendar() {
  const grid = document.getElementById("calendarGrid");
  const currentMonthLabel = document.getElementById("currentMonthLabel");
  
  if (!grid) return;
  
  // Clear existing items but preserve days header
  grid.innerHTML = `
    <div class="cal-day-name">Mon</div>
    <div class="cal-day-name">Tue</div>
    <div class="cal-day-name">Wed</div>
    <div class="cal-day-name">Thu</div>
    <div class="cal-day-name">Fri</div>
    <div class="cal-day-name">Sat</div>
    <div class="cal-day-name">Sun</div>
  `;
  
  currentMonthLabel.innerText = "June 2026";
  
  // June 2026 starts on Monday (1st) and has 30 days
  const startDayIndex = 0; // Monday is 0 index in grid
  const daysInMonth = 30;
  
  // Add empty blocks for days before the 1st (none needed for Mon, June 1 2026)
  
  // Add calendar days
  for (let day = 1; day <= daysInMonth; day++) {
    const dayBtn = document.createElement("button");
    dayBtn.className = "cal-day";
    dayBtn.innerText = day;
    
    // Construct Date String YYYY-MM-DD
    const dateStr = `2026-06-${day < 10 ? '0' + day : day}`;
    
    // Classify based on mock database state
    if (state.attendance[dateStr]) {
      const status = state.attendance[dateStr];
      if (status === "P") dayBtn.classList.add("present");
      else if (status === "A") dayBtn.classList.add("absent");
      else if (status === "L") dayBtn.classList.add("leave");
    }
    
    if (dateStr === state.selectedDate) {
      dayBtn.classList.add("selected");
    }
    
    dayBtn.addEventListener("click", () => {
      // Set selected
      document.querySelectorAll(".cal-day").forEach(el => el.classList.remove("selected"));
      dayBtn.classList.add("selected");
      state.selectedDate = dateStr;
      document.getElementById("selectedDateLabel").innerText = `Selected Date: ${dateStr}`;
    });
    
    grid.appendChild(dayBtn);
  }
  
  // Handle marking actions
  setupAttendanceActions();
}

function setupAttendanceActions() {
  const markPresent = document.getElementById("btnMarkPresent");
  const markAbsent = document.getElementById("btnMarkAbsent");
  const markLeave = document.getElementById("btnMarkLeave");
  
  // Remove duplicate listeners
  const newMarkPresent = markPresent.cloneNode(true);
  const newMarkAbsent = markAbsent.cloneNode(true);
  const newMarkLeave = markLeave.cloneNode(true);
  
  markPresent.parentNode.replaceChild(newMarkPresent, markPresent);
  markAbsent.parentNode.replaceChild(newMarkAbsent, markAbsent);
  markLeave.parentNode.replaceChild(newMarkLeave, markLeave);
  
  newMarkPresent.addEventListener("click", () => recordAttendance("P"));
  newMarkAbsent.addEventListener("click", () => recordAttendance("A"));
  newMarkLeave.addEventListener("click", () => recordAttendance("L"));
}

function recordAttendance(status) {
  state.attendance[state.selectedDate] = status;
  buildCalendar();
  renderAttendanceTable();
  alert(`Attendance successfully marked as ${status === 'P' ? 'Present' : status === 'A' ? 'Absent' : 'Leave'} for date ${state.selectedDate}.`);
}

function renderAttendanceTable() {
  const tbody = document.getElementById("attendanceLogsBody");
  if (!tbody) return;
  
  tbody.innerHTML = "";
  
  // Sort dates descending
  const sortedDates = Object.keys(state.attendance).sort((a, b) => new Date(b) - new Date(a));
  
  sortedDates.forEach(date => {
    const status = state.attendance[date];
    const tr = document.createElement("tr");
    
    let statusText = "Present";
    let statusClass = "badge-approved";
    if (status === "A") { statusText = "Absent"; statusClass = "badge-rejected"; }
    else if (status === "L") { statusText = "Leave"; statusClass = "badge-pending"; }
    
    tr.innerHTML = `
      <td>${date}</td>
      <td><span class="badge ${statusClass}">${statusText}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// Outpass submission Form
function setupOutpassForm() {
  const form = document.getElementById("outpassForm");
  if (!form) return;
  
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const startDate = document.getElementById("outpassStartDate").value;
    const endDate = document.getElementById("outpassEndDate").value;
    const reason = document.getElementById("outpassReason").value.trim();
    
    if (!startDate || !endDate || !reason) {
      alert("Please fill in all outpass request fields.");
      return;
    }
    
    if (new Date(startDate) > new Date(endDate)) {
      alert("Start date cannot be after end date!");
      return;
    }
    
    // Add pending outpass request to list
    const newRequest = {
      id: state.outpassRequests.length + 1,
      userId: state.hosteller.id || 101,
      firstName: state.hosteller.firstName,
      lastName: state.hosteller.lastName,
      requestDate: new Date().toISOString().slice(0, 16).replace("T", " "),
      startDate: startDate,
      endDate: endDate,
      reason: reason,
      status: "Pending"
    };
    
    state.outpassRequests.unshift(newRequest);
    
    // Reset Form
    form.reset();
    
    // Re-render
    renderOutpassHistoryHosteller();
    alert("Outpass request successfully submitted to the warden!");
  });
}

function renderOutpassHistoryHosteller() {
  const tbody = document.getElementById("outpassHistoryBody");
  if (!tbody) return;
  
  tbody.innerHTML = "";
  
  // Filter for only John Doe's requests (user_id 101)
  const myRequests = state.outpassRequests.filter(req => req.userId === 101);
  
  if (myRequests.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:var(--text-muted);">No outpass requests found.</td></tr>`;
    return;
  }
  
  myRequests.forEach(req => {
    const tr = document.createElement("tr");
    
    let statusClass = "badge-pending";
    if (req.status === "Approved") statusClass = "badge-approved";
    else if (req.status === "Rejected") statusClass = "badge-rejected";
    
    tr.innerHTML = `
      <td>${req.startDate} to ${req.endDate}</td>
      <td>${req.reason}</td>
      <td>${req.requestDate}</td>
      <td><span class="badge ${statusClass}">${req.status}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// ==========================================
// WARDEN PORTAL FUNCTIONS
// ==========================================

function renderWardenStats() {
  // Stat calculations
  const totalHostellers = state.hostellersList.length;
  
  // Pending outpasses count
  const pendingCount = state.outpassRequests.filter(r => r.status === "Pending").length;
  
  // Today's attendance percentage (June 6, 2026)
  // Let's count how many students have attendance marked for 2026-06-06 and are present
  // For the simulator, let's mock attendance rates
  const presentCount = Object.values(state.attendance).filter(s => s === "P").length;
  const totalDaysMarked = Object.keys(state.attendance).length;
  const attendanceRate = totalDaysMarked > 0 ? Math.round((presentCount / totalDaysMarked) * 100) : 85;
  
  // Birthdays count
  // June 6 is the mock date
  const todayBirthdays = state.hostellersList.filter(h => h.dob.includes("06-06")).length;
  
  document.getElementById("statTotalStudents").innerText = totalHostellers;
  document.getElementById("statAttendanceRate").innerText = attendanceRate + "%";
  document.getElementById("statPendingOutpasses").innerText = pendingCount;
  document.getElementById("statTodayBirthdays").innerText = todayBirthdays;
}

// Render Outpass Approvals lists (Wardens view)
function renderOutpassApprovalQueue() {
  const container = document.getElementById("approvalQueueContainer");
  if (!container) return;
  
  container.innerHTML = "";
  
  const pendingRequests = state.outpassRequests.filter(r => r.status === "Pending");
  
  if (pendingRequests.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted);">No pending outpass requests in queue.</div>`;
    return;
  }
  
  pendingRequests.forEach(req => {
    const card = document.createElement("div");
    card.className = "approval-item";
    
    card.innerHTML = `
      <div class="approval-info">
        <span class="approval-header">${req.firstName} ${req.lastName} (Room ${state.hostellersList.find(h=>h.id===req.userId)?.room || 'N/A'})</span>
        <span class="approval-dates">Dates: <strong>${req.startDate}</strong> to <strong>${req.endDate}</strong> (Req: ${req.requestDate})</span>
        <span class="approval-reason">"${req.reason}"</span>
      </div>
      <div class="approval-actions">
        <button class="action-btn btn-approve" onclick="processOutpass(${req.id}, 'Approved')">Approve</button>
        <button class="action-btn btn-reject" onclick="processOutpass(${req.id}, 'Rejected')">Reject</button>
      </div>
    `;
    
    container.appendChild(card);
  });
}

// Expose process outpass globally so click actions can trigger
window.processOutpass = function(reqId, status) {
  const req = state.outpassRequests.find(r => r.id === reqId);
  if (req) {
    req.status = status;
    renderOutpassApprovalQueue();
    renderWardenStats();
    alert(`Outpass Request ID #${reqId} has been ${status}.`);
  }
};

// Birthday Alerts block in Warden
function renderBirthdayAlerts() {
  const container = document.getElementById("birthdayAlertsContainer");
  if (!container) return;
  
  // Find who has birthday on June 6th
  const birthdayKids = state.hostellersList.filter(h => h.dob.endsWith("06-06"));
  
  if (birthdayKids.length === 0) {
    container.innerHTML = `<p style="color:var(--text-muted); font-size:0.875rem;">No birthdays today.</p>`;
    return;
  }
  
  container.innerHTML = birthdayKids.map(kid => `
    <div style="background: rgba(245, 158, 11, 0.05); border: 1px dashed rgba(245, 158, 11, 0.2); padding:0.75rem; border-radius: var(--radius-sm); font-size:0.85rem; display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.5rem;">
      <div>
        <strong>🎉 ${kid.firstName} ${kid.lastName}</strong>
        <div style="color:var(--text-muted); font-size:0.75rem;">Hostel: ${kid.hostel} | Room: ${kid.room}</div>
      </div>
      <span style="color:var(--warning); font-weight:600; font-size:0.75rem;">Send Email Alerts</span>
    </div>
  `).join("");
}

// Student roster filter & render
function renderStudentRosterTable(filteredStudents = state.hostellersList) {
  const tbody = document.getElementById("studentRosterBody");
  if (!tbody) return;
  
  tbody.innerHTML = "";
  
  if (filteredStudents.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:1rem;">No matching students found.</td></tr>`;
    return;
  }
  
  filteredStudents.forEach(s => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${s.id}</td>
      <td><strong>${s.firstName} ${s.lastName}</strong></td>
      <td>${s.email}</td>
      <td>${s.hostel}</td>
      <td>${s.room}</td>
      <td>${s.dept}</td>
      <td>${s.year}</td>
    `;
    tbody.appendChild(tr);
  });
  
  const countLabel = document.getElementById("filteredCountLabel");
  if (countLabel) {
    countLabel.innerText = `Total Hostellers Found: ${filteredStudents.length}`;
  }
}

// Hook filter selections
function setupStudentFilter() {
  const btnApply = document.getElementById("btnApplyFilter");
  if (!btnApply) return;
  
  btnApply.addEventListener("click", () => {
    const hostelVal = document.getElementById("filterHostel").value;
    const deptVal = document.getElementById("filterDept").value;
    const yearVal = document.getElementById("filterYear").value;
    
    const results = state.hostellersList.filter(student => {
      const matchHostel = (hostelVal === "All Hostels") || (student.hostel === hostelVal);
      const matchDept = (deptVal === "All Departments") || (student.dept === deptVal);
      const matchYear = (yearVal === "All Years") || (student.year === yearVal);
      
      return matchHostel && matchDept && matchYear;
    });
    
    renderStudentRosterTable(results);
  });
}
