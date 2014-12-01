package com.atteq.asl.tasks;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;

import org.apache.commons.codec.binary.Hex;
import org.codehaus.jackson.annotate.JsonProperty;

import com.atteq.asl.AtteqServiceLayerImpl;
import com.atteq.asl.utils.StringHelper;

public class SecuredTask extends Task {

	static class SecurityInfo {

		final String randomToken;

		final String hashedToken;

		public SecurityInfo(String secureToken) throws NoSuchAlgorithmException {
			this.randomToken = StringHelper.getRandomString(32);
			this.hashedToken = sha1(randomToken + secureToken);
		}

		private static String sha1(String data) throws NoSuchAlgorithmException {
			MessageDigest digest = MessageDigest.getInstance("SHA-1");
			byte[] digestResult = digest.digest(data.getBytes());
			return Hex.encodeHexString(digestResult).toUpperCase();
		}

		@JsonProperty("random_token")
		public String getRandomToken() {
			return randomToken;
		}

		@JsonProperty("hashed_token")
		public String getHashedToken() {
			return hashedToken;
		}

	}

	private SecurityInfo securityInfo;

	public SecuredTask(String name, Object data, AtteqServiceLayerImpl asl) throws NoSuchAlgorithmException {
		super(name, data);
		this.securityInfo = new SecurityInfo(asl.getSecurityToken());
	}

	public Object getData() {
		HashMap<String, Object> map = new HashMap<String, Object>();
		map.put("data", super.getData());
		map.put("security", securityInfo);
		return map;
	}

}