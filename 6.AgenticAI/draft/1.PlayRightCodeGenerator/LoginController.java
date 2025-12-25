package org.dnyanyog.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.dnyanyog.dto.request.LoginRequest;
import org.dnyanyog.dto.response.LoginResponse;
import org.dnyanyog.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoginController {
	@Autowired
	private LoginService loginService;
	private static final Logger logger = LoggerFactory.getLogger(LoginController.class);

	// @PostMapping("/api/auth/v1/login")
	// public ResponseEntity<LoginResponse> loginUser(@RequestBody LoginRequest request) {
	// 	logger.info("Login User");
	// 	return loginService.loginUser(request);
	// }

	@GetMapping(path = "/api/auth/v2/wake-up")
  public ResponseEntity<String> wakeUp() {
    return new ResponseEntity<>("woke-up", HttpStatus.OK);
  }

	@PostMapping("/api/auth/v2/login")
	public ResponseEntity<LoginResponse> loginUserV2(@RequestBody LoginRequest request) {
		logger.info("Login User");
		return loginService.loginUser(request);
	}

}
