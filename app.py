
import streamlit as st
from datetime import date, datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Shiftwell | Workforce Operations",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# SESSION STATE
# =========================================================
if "review_history" not in st.session_state:
    st.session_state.review_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "certificate_history" not in st.session_state:
    st.session_state.certificate_history = []

if "request_counter" not in st.session_state:
    st.session_state.request_counter = 1042

# =========================================================
# CUSTOM STYLING
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1020;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #273449;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #F8FAFC;
    }

    p, label, .stMarkdown {
        color: #D1D5DB;
    }

    div[data-testid="stMetric"] {
        background: #151F32;
        border: 1px solid #29374D;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #AAB8CC !important;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    div[data-testid="stForm"] {
        background: #111827;
        border: 1px solid #273449;
        border-radius: 14px;
        padding: 20px;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 42px;
        font-weight: 600;
    }

    .hero {
        background: linear-gradient(120deg, #172554, #14213D);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #30436A;
        margin-bottom: 24px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #CBD5E1;
        font-size: 15px;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("# 📅 Shiftwell")
    st.caption("WORKFORCE MANAGEMENT")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Swap Review",
            "Certificate Checks",
            "Review History",
            "About Project",
        ],
        index=0,
    )

    st.divider()
    st.markdown("### Review policy")
    st.caption("Configured weekly-hours threshold: 48 hours")
    st.caption("Role training confirmation required")
    st.caption("Manual approval remains in control")

    st.divider()
    st.markdown("**Prototype status**")
    st.success("Local demo running")
    st.caption("Sample data only")

# =========================================================
# HELPER: SWAP ELIGIBILITY
# =========================================================
def evaluate_request(
    request_id,
    requester,
    replacement,
    role,
    trained,
    current_hours,
    shift_hours,
):
    """Evaluate configured checks for a proposed swap."""

    projected_hours = current_hours + shift_hours
    issues = []

    if not request_id.strip():
        issues.append("A request ID is required.")

    if not requester.strip():
        issues.append("Enter the requesting staff member.")

    if not replacement.strip():
        issues.append("Enter the replacement staff member.")

    if (
        requester.strip()
        and replacement.strip()
        and requester.strip().casefold()
        == replacement.strip().casefold()
    ):
        issues.append(
            "Requester and replacement must be different."
        )

    if not trained:
        issues.append(
            f"Training eligibility for the {role} role "
            "is not confirmed."
        )

    if projected_hours > 48:
        issues.append(
            f"Projected weekly hours are {projected_hours}, "
            "above the configured 48-hour threshold."
        )

    return projected_hours, issues


# =========================================================
# PAGE 1: OVERVIEW
# =========================================================
if page == "Overview":
    st.title("Workforce Operations")
    st.caption(
        "A quick view of the Shiftwell prototype."
    )

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Welcome to Shiftwell</div>
            <p class="hero-subtitle">
                Help managers review shift swaps consistently
                and identify certificate records requiring attention.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reviews = st.session_state.review_history
    certificates = st.session_state.certificate_history

    total_reviews = len(reviews)
    flagged_reviews = sum(
        1 for item in reviews if item["issues"]
    )
    ready_reviews = total_reviews - flagged_reviews

    expired_certificates = sum(
        1 for item in certificates
        if item["status"] == "Expired"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Swap checks", total_reviews)
    c2.metric("Ready for next step", ready_reviews)
    c3.metric("Swap reviews flagged", flagged_reviews)
    c4.metric("Expired records flagged", expired_certificates)

    st.divider()
    st.subheader("How Shiftwell works")

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 01 · Capture")
        st.write(
            "Enter the swap request and relevant scheduling details."
        )

    with b:
        st.markdown("### 02 · Validate")
        st.write(
            "Check training confirmation, projected hours, "
            "and certificate-expiry information."
        )

    with c:
        st.markdown("### 03 · Review")
        st.write(
            "Explain failed checks so an authorized person "
            "can decide what happens next."
        )

    st.info(
        "Demonstration only. No live roster, employee database, "
        "or certificate authority is connected."
    )

    st.subheader("Quick navigation")

    q1, q2 = st.columns(2)

    with q1:
        st.markdown("**Smart Swap Review**")
        st.write(
            "Evaluate training confirmation and projected weekly hours."
        )

    with q2:
        st.markdown("**Certificate Checks**")
        st.write(
            "Flag missing or expired certificate records."
        )


# =========================================================
# PAGE 2: SWAP REVIEW
# =========================================================
elif page == "Swap Review":
    st.title("Smart Swap Review")
    st.caption(
        "Evaluate a proposed shift swap before roster changes."
    )

    st.info(
        "Passing these simplified checks does not approve a swap. "
        "A manager must still make the final decision."
    )

    with st.form("swap_review_form"):
        st.subheader("01 · Swap details")

        c1, c2 = st.columns(2)

        with c1:
            request_id = st.text_input(
                "Request ID",
                value=f"SW-{st.session_state.request_counter}",
            )

            requester = st.text_input(
                "Requesting staff member",
                value="Ananya Rao",
            )

            replacement = st.text_input(
                "Replacement staff member",
                value="Rahul Kumar",
            )

        with c2:
            role = st.selectbox(
                "Shift role",
                ["Nurse", "Cook", "Store Associate"],
            )

            trained = st.checkbox(
                "Replacement is trained for this role",
                value=True,
            )

        st.divider()
        st.subheader("02 · Working-hours check")

        h1, h2 = st.columns(2)

        with h1:
            current_hours = st.number_input(
                "Replacement's existing weekly hours",
                min_value=0,
                max_value=80,
                value=36,
                step=1,
            )

        with h2:
            shift_hours = st.number_input(
                "Proposed shift duration (hours)",
                min_value=1,
                max_value=24,
                value=8,
                step=1,
            )

        projected = current_hours + shift_hours

        st.metric(
            "Projected weekly hours",
            f"{projected} hours",
            delta=f"{projected - 48:+} hours vs threshold",
            delta_color="inverse",
        )

        submitted = st.form_submit_button(
            "Run eligibility checks",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        projected_hours, issues = evaluate_request(
            request_id,
            requester,
            replacement,
            role,
            trained,
            current_hours,
            shift_hours,
        )

        result = {
            "request_id": request_id.strip(),
            "requester": requester.strip(),
            "replacement": replacement.strip(),
            "role": role,
            "projected_hours": projected_hours,
            "issues": issues.copy(),
            "timestamp": datetime.now().strftime(
                "%d %b %Y, %H:%M"
            ),
        }

        st.session_state.last_result = result
        st.session_state.review_history.insert(0, result)
        st.session_state.request_counter += 1

    result = st.session_state.last_result

    if result is not None:
        st.divider()
        st.subheader("03 · Review decision")

        if result["issues"]:
            st.error("Further review required")

            for issue in result["issues"]:
                st.markdown(f"- {issue}")

            st.warning(
                "Resolve flagged issues and have an authorized "
                "manager review the request."
            )
        else:
            st.success("No configured checks failed.")

            st.write(
                "The request is ready for the next approval step. "
                "It has not been automatically approved."
            )

        st.caption(
            f"Last evaluated: {result['timestamp']} · "
            f"Request: {result['request_id']}"
        )


# =========================================================
# PAGE 3: CERTIFICATE CHECKS
# =========================================================
elif page == "Certificate Checks":
    st.title("Certificate Compliance")
    st.caption(
        "CarePoint Clinics · Certificate-expiry demonstration"
    )

    st.info(
        "Enter sample credential information to demonstrate "
        "how expired or missing records can be flagged."
    )

    with st.form("certificate_form"):
        staff_name = st.text_input(
            "Staff member",
            value="Priya Sharma",
        )

        role = st.selectbox(
            "Staff role",
            ["Nurse", "Doctor", "Clinic Assistant"],
        )

        certificate_type = st.selectbox(
            "Required credential",
            [
                "BLS Certificate",
                "Nursing Council Registration",
                "Other",
            ],
        )

        expiry_date = st.date_input(
            "Certificate expiry date",
            value=date.today(),
        )

        certificate_present = st.checkbox(
            "Certificate record is available",
            value=True,
        )

        check_certificate = st.form_submit_button(
            "Check certificate",
            type="primary",
            use_container_width=True,
        )

    if check_certificate:
        if not staff_name.strip():
            status = "Missing"
            message = "Enter the staff member's name."

        elif not certificate_present:
            status = "Missing"
            message = (
                "Certificate record is missing. "
                "Do not treat this credential as verified."
            )

        elif expiry_date < date.today():
            status = "Expired"
            message = (
                f"{certificate_type} expired on "
                f"{expiry_date.strftime('%d %b %Y')}."
            )

        else:
            status = "Date not past"
            message = (
                "The entered expiry date is not in the past. "
                "Authenticity and other role requirements remain "
                "unverified."
            )

        record = {
            "staff_name": staff_name.strip(),
            "role": role,
            "certificate_type": certificate_type,
            "expiry_date": expiry_date.strftime("%d %b %Y"),
            "status": status,
            "message": message,
            "timestamp": datetime.now().strftime(
                "%d %b %Y, %H:%M"
            ),
        }

        st.session_state.certificate_history.insert(0, record)
        st.session_state.last_certificate_result = record

    certificate_result = st.session_state.get(
        "last_certificate_result"
    )

    if certificate_result is not None:
        st.divider()
        st.subheader("Certificate check result")

        st.write(
            f"**Staff:** {certificate_result['staff_name']}"
        )
        st.write(
            f"**Role:** {certificate_result['role']}"
        )
        st.write(
            f"**Credential:** "
            f"{certificate_result['certificate_type']}"
        )
        st.write(
            f"**Expiry date:** {certificate_result['expiry_date']}"
        )

        if certificate_result["status"] == "Expired":
            st.error(certificate_result["message"])
            st.warning(
                "Flag the record for verification before scheduling."
            )

        elif certificate_result["status"] == "Missing":
            st.error(certificate_result["message"])

        else:
            st.success(certificate_result["message"])
            st.info(
                "This result is not proof of certificate authenticity."
            )

    st.divider()
    st.subheader("Certificate check history")

    if st.session_state.certificate_history:
        certificate_rows = [
            {
                "Staff": item["staff_name"],
                "Role": item["role"],
                "Credential": item["certificate_type"],
                "Expiry": item["expiry_date"],
                "Result": item["status"],
                "Checked at": item["timestamp"],
            }
            for item in st.session_state.certificate_history
        ]

        st.dataframe(
            certificate_rows,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("No certificate checks performed yet.")

    st.caption(
        "Demo only: certificate details are manually entered. "
        "No real certificates or employee records are verified."
    )


# =========================================================
# PAGE 4: REVIEW HISTORY
# =========================================================
elif page == "Review History":
    st.title("Review History")
    st.caption(
        "Swap evaluations performed during this app session."
    )

    history = st.session_state.review_history

    if not history:
        st.info(
            "No swap requests reviewed yet. Open Swap Review "
            "to run your first eligibility check."
        )

    else:
        rows = []

        for item in history:
            rows.append(
                {
                    "Request ID": item["request_id"],
                    "Requester": item["requester"],
                    "Replacement": item["replacement"],
                    "Role": item["role"],
                    "Projected Hours": item["projected_hours"],
                    "Outcome": (
                        "Further review required"
                        if item["issues"]
                        else "Ready for next step"
                    ),
                    "Reviewed At": item["timestamp"],
                }
            )

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

        selected_id = st.selectbox(
            "Inspect request",
            [item["request_id"] for item in history],
        )

        selected = next(
            item
            for item in history
            if item["request_id"] == selected_id
        )

        st.subheader(f"Details: {selected_id}")

        if selected["issues"]:
            for issue in selected["issues"]:
                st.warning(issue)
        else:
            st.success("No configured checks failed.")

    st.divider()
    st.subheader("Session management")

    if st.button("Clear swap review history"):
        st.session_state.review_history = []
        st.session_state.last_result = None
        st.rerun()


# =========================================================
# PAGE 5: ABOUT PROJECT
# =========================================================
elif page == "About Project":
    st.title("About Shiftwell")
    st.caption("Product Intern case-study prototype")

    st.markdown(
        """
        ### Problem being explored

        Shiftwell's case study describes manual shift-swap approvals.
        Managers need to review training eligibility and working hours.
        CarePoint also needs a way to identify expired credential records.

        ### Prototype features

        - Capture a proposed shift swap.
        - Check training confirmation.
        - Calculate projected weekly hours.
        - Flag requests requiring further review.
        - Check manually entered certificate expiry dates.
        - Record evaluation history for the current session.

        ### Limitations

        - Uses manually entered sample data.
        - Does not authenticate users or enforce production permissions.
        - Does not verify certificate authenticity.
        - Does not access a live schedule or employee database.
        - Does not send WhatsApp messages.
        - Does not approve swaps or change rosters automatically.
        - History is session-level, not permanent storage.

        ### Technology

        - Python
        - Streamlit
        - Session state for demo history
        """
    )

    st.warning(
        "The 48-hour threshold is a simplified case-study setting, "
        "not a statement of applicable law or a complete overtime policy."
    )


# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption(
    "Shiftwell · Product case-study demo · Sample data only · "
    "No real scheduling decisions are made."
)
