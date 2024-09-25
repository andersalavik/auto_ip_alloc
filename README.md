
# Auto IP Allocation Plugin for NetBox

Automatically allocate IP addresses from prefixes via REST API in NetBox.

## Table of Contents

- [Auto IP Allocation Plugin for NetBox](#auto-ip-allocation-plugin-for-netbox)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [API Endpoint](#api-endpoint)
    - [Request Parameters](#request-parameters)
    - [Example Requests](#example-requests)
      - [**Allocate an IP Address with Basic Details**](#allocate-an-ip-address-with-basic-details)
      - [**Allocate an IP Address with Additional Fields**](#allocate-an-ip-address-with-additional-fields)
      - [**Allocate and Assign an IP Address to an Interface**](#allocate-and-assign-an-ip-address-to-an-interface)
    - [Response](#response)
    - [Error Handling](#error-handling)
  - [Notes](#notes)
  - [Contact](#contact)

## Introduction

The **Auto IP Allocation Plugin** enhances NetBox by providing an API endpoint to automatically allocate the next available IP address from a specified prefix. It allows you to specify additional fields such as `description`, `dns_name`, `status`, and more when allocating IP addresses, making it a powerful tool for network automation and integration with other systems.

## Features

- Automatically allocate the next available IP address within a prefix.
- Accept additional optional fields to set IP address properties.
- Override inherited fields like `tenant` and `vrf`.
- Assign the IP address to devices, interfaces, or virtual machines.
- Integrate seamlessly with NetBox's REST API.

## Requirements

- **NetBox 4.1** or higher.
- Python 3.8 or higher.
- NetBox plugins enabled in your NetBox installation.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/andersalavik/auto_ip_alloc.git
   ```

2. **Install the Plugin**

   - **Option 1: Development Installation**

     Create a symbolic link to the plugin directory in your NetBox installation:

     ```bash
     ln -s /path/to/auto_ip_alloc /opt/netbox/netbox/netbox/auto_ip_alloc
     ```

   - **Option 2: Install via `pip`**

     Package the plugin and install it:

     ```bash
     cd auto_ip_alloc
     python setup.py sdist
     pip install dist/auto_ip_alloc-0.1.tar.gz
     ```

3. **Enable the Plugin in NetBox Configuration**

   Edit your `configuration.py` (or `configuration.plugins.py`) file:

   ```python
   PLUGINS = [
       'auto_ip_alloc',
   ]

   PLUGINS_CONFIG = {
       'auto_ip_alloc': {},
   }
   ```

4. **Restart NetBox Services**

   ```bash
   # For systemd installations
   sudo systemctl restart netbox
   sudo systemctl restart netbox-rq
   ```

## Configuration

No additional configuration is required. The plugin uses NetBox's REST API framework and permissions.

## Usage

### API Endpoint

**URL:**

```
POST /api/plugins/auto-ip-alloc/allocate-ip/
```

### Request Parameters

- **Required:**

  - `prefix_id` (integer): The ID of the prefix.
  - **OR**
  - `prefix` (string): The prefix in CIDR notation (e.g., `"192.168.1.0/24"`).

- **Optional Fields:**

  - `description` (string): Description of the IP address.
  - `dns_name` (string): DNS name associated with the IP address.
  - `status` (string): Status slug of the IP address (e.g., `"active"`, `"reserved"`).
  - `role` (string): Role slug of the IP address.
  - `tenant` (integer): ID of the tenant.
  - `vrf` (integer): ID of the VRF.
  - `custom_fields` (dictionary): Custom field values.
  - `tags` (list): List of tag slugs or IDs.
  - `assigned_object_type` (string): Content type of the assigned object (e.g., `"dcim.interface"`).
  - `assigned_object_id` (integer): ID of the assigned object.

### Example Requests

#### **Allocate an IP Address with Basic Details**

```bash
curl -X POST \
     -H "Authorization: Token your_api_token" \
     -H "Content-Type: application/json" \
     -d '{
           "prefix": "192.168.1.0/24"
         }' \
     http://your-netbox-instance/api/plugins/auto-ip-alloc/allocate-ip/
```

#### **Allocate an IP Address with Additional Fields**

```bash
curl -X POST \
     -H "Authorization: Token your_api_token" \
     -H "Content-Type: application/json" \
     -d '{
           "prefix": "192.168.1.0/24",
           "description": "Allocated for Server XYZ",
           "dns_name": "server-xyz.example.com",
           "status": "active",
           "tenant": 5,
           "tags": ["production", "web-servers"]
         }' \
     http://your-netbox-instance/api/plugins/auto-ip-alloc/allocate-ip/
```

#### **Allocate and Assign an IP Address to an Interface**

```bash
curl -X POST \
     -H "Authorization: Token your_api_token" \
     -H "Content-Type: application/json" \
     -d '{
           "prefix": "10.0.0.0/24",
           "assigned_object_type": "dcim.interface",
           "assigned_object_id": 123,
           "description": "Assigned to Interface GigabitEthernet0/1"
         }' \
     http://your-netbox-instance/api/plugins/auto-ip-alloc/allocate-ip/
```

### Response

A successful request returns HTTP status `201 Created` and the details of the allocated IP address.

**Example Response:**

```json
{
  "id": 456,
  "url": "http://your-netbox-instance/api/ipam/ip-addresses/456/",
  "family": {
    "value": 4,
    "label": "IPv4"
  },
  "address": "192.168.1.1/24",
  "vrf": null,
  "tenant": {
    "id": 5,
    "url": "http://your-netbox-instance/api/tenancy/tenants/5/",
    "name": "My Tenant",
    "slug": "my-tenant"
  },
  "status": {
    "value": "active",
    "label": "Active"
  },
  "role": null,
  "assigned_object_type": null,
  "assigned_object_id": null,
  "assigned_object": null,
  "nat_inside": null,
  "nat_outside": null,
  "dns_name": "server-xyz.example.com",
  "description": "Allocated for Server XYZ",
  "tags": [
    {
      "id": 2,
      "url": "http://your-netbox-instance/api/extras/tags/2/",
      "name": "production",
      "slug": "production",
      "color": "00ff00"
    },
    {
      "id": 3,
      "url": "http://your-netbox-instance/api/extras/tags/3/",
      "name": "web-servers",
      "slug": "web-servers",
      "color": "0000ff"
    }
  ],
  "custom_fields": {},
  "created": "2023-10-10T12:00:00.000000Z",
  "last_updated": "2023-10-10T12:00:00.000000Z"
}
```

### Error Handling

If any of the provided fields are invalid or the request is malformed, the API returns a `400 Bad Request` with details.

**Example Error Response:**

```json
{
  "tenant": [
    "Invalid pk "999" - object does not exist."
  ],
  "tags": [
    "Object with slug="non-existent-tag" does not exist."
  ],
  "status": [
    ""invalid-status" is not a valid choice."
  ]
}
```

## Notes

- **Authentication:** Ensure you use a valid API token with permissions to create IP addresses.
- **Permissions:** The user associated with the API token must have the necessary permissions in NetBox.
- **Existing Objects:** Make sure that any referenced objects like tenants, VRFs, tags, or assigned objects already exist in NetBox.
- **Assigned Objects:** To assign an IP address to an object, provide both `assigned_object_type` and `assigned_object_id`. The `assigned_object_type` should be in the format `"app_label.model_name"` (e.g., `"dcim.interface"`).
- **Custom Fields:** Include any custom fields defined for the `IPAddress` model in the `custom_fields` dictionary.


## Contact

- **Author:** Anders Alavik
- **Email:** anders.alavik@infracom.se

```