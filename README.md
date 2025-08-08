
# 🚀 Cloud Cost Optimization with AWS Lambda: Deleting Unused EBS Snapshots

Ever created an EC2 instance, used it for a while, and then deleted it—but forgot to delete the snapshot? Yeah, it happens! But if you're managing multiple cloud resources, those forgotten snapshots can silently stack up and burn a hole in your AWS bill 💸. In this post, let's learn a cool (and fun) way to automate their cleanup using AWS Lambda.

---

## 🧠 The Problem

Imagine this:
- A developer spins up an EC2 instance.
- Creates a snapshot of its volume (for backup or reuse).
- Deletes the EC2 instance after use.
- FORGETS to delete the snapshot. 😬

Result? Snapshots are still hanging around in S3 (technically EBS), costing storage dollars for literally no reason.

Manually finding and deleting these is boring and error-prone.

### Solution? Automate It! ⚙️

We’ll create a **Lambda function** in Python that:
1. Fetches all EBS snapshots created by us.
2. Checks whether the snapshots are linked to any volume.
3. Verifies if the volume is attached to any EC2 instance.
4. Deletes snapshots that are stale (i.e. unused/unattached).

---

## 🏗️ Architecture Overview

Here’s what we’ll do:

1. Create a **Lambda Function** in Python.
2. Use **Boto3** (Python AWS SDK) to talk to the EC2 API.
3. Optionally schedule it using **CloudWatch Events**.
4. Give it the right permissions to describe and delete snapshots.

```plaintext
+--------------+
| CloudWatch   | (optional trigger)
+------+-------+
       |
       v
+------+-------+
| AWS Lambda   | ---> Describe Snapshots
| (Python code)| ---> Describe Volumes
|              | ---> Describe Instances
|              | ---> Delete Snapshots
+--------------+
```

---

## 🛠️ Step-by-Step Guide

### 🔹 1. Create a Snapshot Manually (for demo/testing)
- Go to EC2 > Volumes > select one > **Create Snapshot**.
- Delete the EC2 instance. The snapshot stays. (Sneaky, right?)

### 🔹 2. Create the Lambda Function
- Go to AWS Lambda > Create Function.
- Name: `cost-opt-ebs-snapshot`
- Runtime: `Python 3.10`
- Architecture: `x86_64` (default is fine)
- Permissions: Choose default. We’ll fix them later.

### 🔹 3. Add Python Code
Use the main.py source code .

### 🔹 4. Fix Timeout and Permissions

- Go to your Lambda > **Configuration > General Configuration**.
- Edit timeout: Set to `10 seconds` (default is too short).

#### Set Permissions:
- Click **Permissions** in left menu > Click on execution role link.
- Click **Add permissions > Attach policies**.
- Create a custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeSnapshots",
        "ec2:DescribeVolumes",
        "ec2:DescribeInstances",
        "ec2:DeleteSnapshot"
      ],
      "Resource": "*"
    }
  ]
}
```

- Name it something like `CostOptimizationPolicy` and attach it.

### 🔹 5. Test Your Function
- Create a simple test event (empty JSON: `{}`) and run the function.
- Check the **logs in CloudWatch** to see what it did.

---

## ⏰ Optional: Automate with CloudWatch Events
- Go to EventBridge (CloudWatch Events)
- Create a rule to trigger your Lambda every day/week.
- Done! You now have a self-cleaning cloud 🧹

---

## ✅ Pros vs Traditional Manual Method

| Manual Cleanup       | Automated (Lambda)        |
|----------------------|---------------------------|
| Tedious              | Hands-free once deployed  |
| Error-prone          | Accurate & consistent     |
| Requires human time  | Just costs a few ms       |
| Might forget         | Scheduled = no forgetting |

---

## 🏁 Wrapping Up

Cloud cost optimization isn’t always about big redesigns—it’s about *small automation that saves big*. This is one such trick to delete unused EBS snapshots and save on storage.

Hope you enjoyed this hands-on walkthrough. 😄

Stay lean, stay optimized! 💡
