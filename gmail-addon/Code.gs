const UNCOMMON_TLDS = [".xyz", ".top", ".click", ".zip", ".review", ".country", ".stream"];
const LEGITIMATE_DOMAINS = ["example.com", "upwind.io", "company.com"];
const URGENT_KEYWORDS = ["urgent", "immediately", "action required", "verify now", "account suspended"];

function buildHomepage() {
  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("Upwind Phishing Detector"))
    .addSection(
      CardService.newCardSection()
        .addWidget(CardService.newTextParagraph().setText(
          "Open an email in Gmail to scan it for phishing indicators."
        ))
    )
    .build();
}

function scanCurrentMessage(e) {
  GmailApp.setCurrentMessageAccessToken(e.gmail.accessToken);

  const message = GmailApp.getMessageById(e.gmail.messageId);
  const emailContent = buildEmailContent(message);
  const findings = analyzeEmail(emailContent);

  return buildResultsCard(message, findings);
}

function buildEmailContent(message) {
  return [
    "From: " + message.getFrom(),
    "Subject: " + message.getSubject(),
    "",
    message.getPlainBody()
  ].join("\n");
}

function analyzeEmail(emailContent) {
  const findings = [];
  const urls = extractUrls(emailContent);
  const senderEmail = extractSenderEmail(emailContent);

  findings.push(...detectIpBasedUrls(urls));
  findings.push(...detectUncommonDomainUrls(urls));
  findings.push(...detectSpoofedSender(senderEmail));
  findings.push(...detectUrgentLanguage(emailContent));

  return findings;
}

function extractUrls(emailContent) {
  return emailContent.match(/https?:\/\/[^\s<>'"]+/g) || [];
}

function extractSenderEmail(emailContent) {
  const fromMatch = emailContent.match(/^From:\s*(.+)$/mi);

  if (!fromMatch) {
    return null;
  }

  const emailMatch = fromMatch[1].match(/[\w.-]+@[\w.-]+\.\w+/);
  return emailMatch ? emailMatch[0].toLowerCase() : null;
}

function extractDomain(emailAddress) {
  return emailAddress.split("@")[1].toLowerCase();
}

function isIpAddress(value) {
  return /^(\d{1,3}\.){3}\d{1,3}$/.test(value);
}

function getHostname(url) {
  try {
    return new URL(url).hostname;
  } catch (error) {
    return "";
  }
}

function detectIpBasedUrls(urls) {
  return urls
    .filter(url => isIpAddress(getHostname(url)))
    .map(url => "IP address used in URL: " + url);
}

function detectUncommonDomainUrls(urls) {
  return urls
    .filter(url => UNCOMMON_TLDS.some(tld => getHostname(url).endsWith(tld)))
    .map(url => "Uncommon domain used in URL: " + url);
}

function detectSpoofedSender(senderEmail) {
  if (!senderEmail) {
    return [];
  }

  const senderDomain = extractDomain(senderEmail);
  const findings = [];

  LEGITIMATE_DOMAINS.forEach(domain => {
    const similarity = calculateSimilarity(senderDomain, domain);

    if (senderDomain !== domain && similarity >= 0.82) {
      findings.push("Possible spoofed sender: " + senderEmail + " looks similar to " + domain);
    }
  });

  return findings;
}

function detectUrgentLanguage(emailContent) {
  const contentLower = emailContent.toLowerCase();

  return URGENT_KEYWORDS
    .filter(keyword => contentLower.includes(keyword))
    .map(keyword => "Urgent language detected: " + keyword);
}

function calculateSimilarity(firstValue, secondValue) {
  let matches = 0;
  const maxLength = Math.max(firstValue.length, secondValue.length);

  for (let i = 0; i < Math.min(firstValue.length, secondValue.length); i++) {
    if (firstValue[i] === secondValue[i]) {
      matches++;
    }
  }

  return matches / maxLength;
}

function buildResultsCard(message, findings) {
  const isPhishing = findings.length > 0;
  const section = CardService.newCardSection()
    .addWidget(CardService.newTextParagraph().setText(
      "<b>Subject:</b> " + message.getSubject()
    ))
    .addWidget(CardService.newTextParagraph().setText(
      "<b>Likely phishing attempt:</b> " + (isPhishing ? "YES" : "NO")
    ))
    .addWidget(CardService.newTextParagraph().setText(
      "<b>Detected indicators:</b> " + findings.length
    ));

  if (findings.length > 0) {
    findings.forEach(finding => {
      section.addWidget(CardService.newTextParagraph().setText("• " + finding));
    });
  } else {
    section.addWidget(CardService.newTextParagraph().setText("No suspicious indicators detected."));
  }

  return CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("Phishing Scan Results"))
    .addSection(section)
    .build();
}
