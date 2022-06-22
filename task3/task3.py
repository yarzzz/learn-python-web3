from typing import Any, Dict

from eth_utils import (
    encode_hex,
    function_signature_to_4byte_selector,
    event_signature_to_log_topic
)
from loguru import logger

erc20_signatures = {
    "functions": [
        "name()",
        "symbol()",
        "decimals()",
        "totalSupply()",
        "balanceOf(address)",
        "transfer(address, uint256)",
        "transferFrom(address, address, uint256)",
        "approve(address, uint256)",
        "allowance(address, address)"
    ],
    "events": [
        "Transfer(address, address, uint256)",
        "Approval(address, address, uint256)"
    ]
}

erc721_signatures = {
    "functions": [
        "balanceOf(address)",
        "ownerOf(uint256)",
        "safeTransferFrom(address, address, uint256, bytes)",
        "safeTransferFrom(address, address, uint256)",
        "transferFrom(address, address, uint256)",
        "approve(address, uint256)",
        "setApprovalForAll(address, bool)",
        "getApproved(uint256)",
        "isApprovedForAll(address, address)"
    ],
    "events": [
        "Transfer(address, address, uint256)",
        "Approval(address, address, uint256)",
        "ApprovalForAll(address, address, bool)"
    ]
}

erc1155_signatures = {
    "functions": [
        "safeTransferFrom(address, address, uint256, uint256, bytes)",
        "safeBatchTransferFrom(address, address, uint256[], uint256[], bytes)",
        "balanceOf(address, uint256)",
        "balanceOfBatch(address[], uint256[])",
        "setApprovalForAll(address, bool)",
        "isApprovedForAll(address, address)"
    ],
    "events": [
        "TransferSingle(address, address, address, uint256, uint256)",
        "TransferBatch(address, address, address, uint256[], uint256[])",
        "ApprovalForAll(address, address, bool)",
        "URI(string, uint256)"
    ]
}

all_signatures = {
    "erc20": erc20_signatures,
    "erc721": erc721_signatures,
    "erc1155": erc1155_signatures
}

def main():
    for erc in all_signatures:
        signatures = all_signatures[erc]
        for function_signature in signatures["functions"]:
            selector = encode_hex(function_signature_to_4byte_selector(function_signature.replace(" ", "")))
            logger.info("function: erc: %s, signature: %s, selector: %s" % (erc, function_signature, selector))
        for event_signature in signatures["events"]:
            topic = encode_hex(event_signature_to_log_topic(event_signature))
            logger.info("event: erc: %s, signature: %s topic: %s" % (erc, event_signature, topic))

if __name__ == '__main__':
    main()
